from datetime import datetime
from tqdm import tqdm
import networkx as nx
import pandas as pd
import argparse
import json
import os
import re



class TelegramMessage:
	def __init__(self, msg):
		self.msg = msg
		
	def setMsg(self, msg):
		self.msg = msg
		
	def getMessageID(self):
		return self.msg['id']


	def getMessageText(self):
		return self.msg['message']

	def getMessageChannelID(self):
		return self.msg['peer_id']['channel_id']

	def getMessageTime(self):
		return self.msg['date']

	def getForwardedFrom(self):
		if 'fwd_from' in self.msg and self.msg['fwd_from'] is not None:
			return self.msg['fwd_from']
		return None

	def getForwardedFromChannelID(self):
		if 'fwd_from' in self.msg and self.msg['fwd_from'] is not None and self.msg['fwd_from']['from_id'] is not None:
			if 'channel_id' in self.msg['fwd_from']['from_id']:
				return self.msg['fwd_from']['from_id']['channel_id'] # there is also user_id sometimes -> need to be verified
		return None

	def getForwardedFromTime(self):
		if 'fwd_from' in self.msg and self.msg['fwd_from'] is not None:
			return self.msg['fwd_from']['date']
		return None

	def getForwardedFromMessageID(self):
		if 'fwd_from' in self.msg and self.msg['fwd_from'] is not None:
			return self.msg['fwd_from']['channel_post']
		return None

	def getEntities(self):
		if 'entities' in self.msg:
			self.resolveEntities()
			return self.msg['entities'] 
		else:
			return []


	def __decode_unicode_escape_sequences(self,text):
		return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)


	def resolveEntities(self):
		if 'entities' in self.msg:
			msg_text = self.msg['message']
			msg_text = msg_text.replace('\n', ' ')
				
			entities_resolved = []
			for entity in self.msg['entities']:
				offset = entity['offset']
				length = entity['length']
				entity_text = msg_text[offset:offset+length]
				entity['entity_text'] = entity_text
				entities_resolved += [entity]
			
			self.msg['entities'] = entities_resolved

	def getMsg(self):
		return self.msg


class TelegramToolkit:
	def __init__(self, messages_collection_dir, out_dir):
		self.messages_collection_dir = messages_collection_dir
		self.out_dir = out_dir
		self.channel_to_channel_graph = nx.DiGraph()

	def set_messages_collection_dir(self, messages_collection_dir):
		self.messages_collection_dir = messages_collection_dir


	def save_channel_to_channel_graph(self, graph_name):
		nx.write_gml(self.channel_to_channel_graph, self.out_dir + graph_name + '.gml')

	def create_channel_to_channel_graph(self):
		print('#\tChannel to channel graph construction\t#')
		for file in tqdm(os.listdir(self.messages_collection_dir)):
			#print('>>\t\tprocessing:', file)
			with open(self.messages_collection_dir + file, 'r') as fi:
				for line in fi:
					msg = json.loads(line)
					tmsg = TelegramMessage(msg)

					if tmsg.getForwardedFrom() is not None:
						source = tmsg.getForwardedFromChannelID()
						dest = tmsg.getMessageChannelID()
						time_point = tmsg.getForwardedFromTime()

						if source is not None and dest is not None:
							if source not in self.channel_to_channel_graph:
								self.channel_to_channel_graph.add_node(source)
							if dest not in self.channel_to_channel_graph:
								self.channel_to_channel_graph.add_node(dest)

							if (source, dest) in self.channel_to_channel_graph.edges():
								self.channel_to_channel_graph.edges[source,dest]['time'] += [time_point]
							else:
								self.channel_to_channel_graph.add_edge(source, dest, time=[time_point])



	def create_msg_chain(self, message_chain_name):
		print('#\tMessage chain construction\t#')
		msg_chain = {}
		for file in tqdm(os.listdir(self.messages_collection_dir)):
			with open(self.messages_collection_dir + file, 'r') as fi:
				for line in fi:
					msg = json.loads(line)

					tmsg = TelegramMessage(msg)
					fwd_from = tmsg.getForwardedFrom()
					if fwd_from is not None:
						dest_message_id = tmsg.getMessageID()
						dest_channel_id = tmsg.getMessageChannelID()
						source_channel_id = tmsg.getForwardedFromChannelID()
						source_message_id = fwd_from['channel_post']
						time = tmsg.getMessageTime()
						message_text = tmsg.getMessageText()
						
						if source_channel_id is not None and source_message_id is not None:
							if (source_message_id, source_channel_id) not in msg_chain:
								msg_chain[(source_message_id, source_channel_id)] = []
							msg_chain[(source_message_id, source_channel_id)] += [{'source_message_id': source_message_id, \
																					'source_channel_id': source_channel_id,
																					'dest_message_id': dest_message_id,
																					'dest_channel_id': dest_channel_id,
																					'time': time,
																					'message_text': message_text}]

		msg_chain_list = [x for k,v in msg_chain.items() for x in v]
		df = pd.DataFrame.from_dict(msg_chain_list)
		df.to_csv(self.out_dir + message_chain_name + '.csv')		
					


	def explicit_msg_entities(self):
		print('#\tEntities Explicitation\t#')
		for file in tqdm(list(os.listdir(self.messages_collection_dir))):
			#print(file)
			with open(self.messages_collection_dir + file, 'r') as fi:
				with open(self.out_dir + file, 'w+') as fo:
					for line in fi:
						msg = json.loads(line)
						tmsg = TelegramMessage(msg)
						tmsg.resolveEntities()
						json.dump(tmsg.getMsg(), fo)
						fo.write('\n')



	def compute_entity_frequency(self, th, use_type, dest):
		print('#\tEntity Frequency\t#')
		ecount = {}
		for file in tqdm(list(os.listdir(self.messages_collection_dir))):
			with open(self.messages_collection_dir + file, 'r') as fi:
				for line in fi:
					msg = json.loads(line)
					tmsg = TelegramMessage(msg)
					entities = tmsg.getEntities()
					for entity in entities:
						entity_text = entity['entity_text'].strip()
						entity_type = entity['_']

						if use_type:
							if (entity_text, entity_type) not in ecount:
								ecount[(entity_text, entity_type)] = 0
							ecount[(entity_text, entity_type)] += 1	
						else:
							if entity_text not in ecount:
								ecount[entity_text] = 0
							ecount[entity_text] += 1
		ecount = dict([(str(entity), count) for (entity, count) in sorted(ecount.items(), key=lambda x : x[1], reverse=True) if count >= th ])

		with open(self.out_dir + dest + '.json', 'w+', encoding='utf-8') as fo:
			json.dump(ecount, fo, ensure_ascii=False, indent=4)
						


	def computer_entity_frequency_over_channels(self, th, use_type, dest):
		print('#\tEntity Frequency over Channels\t#')
		channel2dist = {}
		for file in tqdm(list(os.listdir(self.messages_collection_dir))):
			dist = {}
			channel_id = file.replace('.txt', '').split('_')[-1]
			with open(self.messages_collection_dir + file, 'r') as fi:
				for line in fi:
					msg = json.loads(line)
					tmsg = TelegramMessage(msg)
					entities = tmsg.getEntities()
					for entity in entities:
						entity_text = entity['entity_text'].strip()
						entity_type = entity['_']
						if use_type:
							if (entity_text, entity_type) not in dist:
								dist[(entity_text, entity_type)] = 0
							dist[(entity_text, entity_type)] += 1	
						else:
							if entity_text not in dist:
								dist[entity_text] = 0
							dist[entity_text] += 1

				dist = dict([(str(entity), count) for (entity, count) in sorted(dist.items(), key=lambda x : x[1], reverse=True) if count >= th ])
				channel2dist[channel_id] = dist

			with open(self.out_dir + dest + '.jsonl', 'w+', encoding='utf-8') as fo:
				for channel_id, dist in channel2dist.items():
					json.dump({'channel id': channel_id, 'entity distribution': dist}, fo, ensure_ascii=False)	
					fo.write('\n')	

if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Telegram Toolkit Commands')
	parser.add_argument('-i', '--input-data-dir', dest='input_data_dir', default='data/', type=str, action='store', help='The input directory containing raw data from Telegram. Default: \'data/\'')
	parser.add_argument('-o', '--output-data-dir', dest='output_data_dir', default='out/', type=str, action='store', help='The output directory where the results will be saved. Default: \'out/\'')
	
	parser.add_argument('-re', '--resolve-entities', dest='resolve_entity_flag', action='store_true', help='Resolve the entities in the raw Telegram data collection.')
	
	parser.add_argument('-ccg', '--create-channel-graph', dest='create_channel_graph_flag', action='store_true', help='Create the channel-to-channel graph from the Telegram data collection.')
	parser.add_argument('-cmc', '--create-message-chain', dest='create_message_chain_flag', action='store_true', help='Create the message chains of the messages from the Telegram data collection.')
	parser.add_argument('-gn', '--graph-name', dest='graph_name', default='mygraph', action='store', help='Name of the graph created using the \'-ccg\' or \'--create-channel-graph\' option. Default: mygraph')
	parser.add_argument('-mcn', '--message-chain-name', dest='message_chain_name', default='my_message_chain', action='store', help='Name of the CSV file containing the information to which channels a message was forwarded to. It only works with either \'-cmc\' or \'--create-message-chain\' option. Default: my_message_chain')
	
	parser.add_argument('-ef', '--entity-frequency', dest='entity_frequency_flag', action='store_true', help='Compute the frequency of the entities on the whole data.')
	parser.add_argument('-efth', '--entity-frequency-threshold', dest='entity_frequency_threshold', default='1', action='store', help='Threshold to cut the entity frequency. Only entities appearing a number of times equal to or greater than the threshold are saved. It only works with either \'-ef\' or \'--entity-frequency\' option. Default: 1')
	parser.add_argument('-eft', '--entity-frequency-type', dest='entity_frequency_type', action='store_true', help='The Telegram Toolkit will consider the entity type while computing the entity frequency. It only works with either \'-ef\' or \'--entity-frequency\' option.')
	parser.add_argument('-efs', '--entity-frequency-save', dest='entity_frequency_dest', default='entity_frequency', action='store', help='The output file containing the entity frequency. It only works with either \'-ef\' or \'--entity-frequency\' option. Default: entity_frequency')
	
	parser.add_argument('-efc', '--entity-frequency-channel', dest='entity_frequency_channel_flag', action='store_true', help='Compute the frequency of the entities over channels.')
	parser.add_argument('-efcth', '--entity-frequency-channel-threshold', dest='entity_frequency_channel_threshold', default='1', action='store', help='Threshold to cut the entity frequency over channels. Only entities appearing a number of times equal to or greater than the threshold are saved. It only works with either \'-efc\' or \'--entity-frequency-channel\' option. Default: 1')
	parser.add_argument('-efct', '--entity-frequency-channel-type', dest='entity_frequency_channel_type', action='store_true', help='The Telegram Toolkit will consider the entity type while computing the entity frequency over channels. It only works with either \'-efc\' or \'--entity-frequency-channel\' option.')
	parser.add_argument('-efcs', '--entity-frequency-channel-save', dest='entity_frequency_channel_dest', default='entity_frequency_channels', action='store', help='The output file containing the entity frequency over channels. It only works with either \'-efc\' or \'--entity-frequency-channel\' option. Default: entity_frequency_over_channels')

	#parser.add_argument('-edc', '--entity-distribution-channel', dest='entity_distribution_channel_flag', action='store_true', help='Compute the distribution of the entities over channels.')
	#parser.add_argument('-edth', '--entity-distribution-threshold', dest='entity_distribution_threshold', default='1', action='store', help='Threshold to cut the entity distribution over channels. Only entities appearing a number of times equal to or greater than the threshold are saved. It only works with either \'-edc\' or \'--entity-distribution-channel\' option. Default: 1')
	#parser.add_argument('-edt', '--entity-distribution-type', dest='entity_distribution_type', action='store_true', help='The Telegram Toolkit will consider the entity type while computing the entity distribution over channels. It only works with either \'-edc\' or \'--entity-distribution-channel\' option.')
	#parser.add_argument('-eds', '--entity-distribution-save', dest='entity_distribution_dest', default='entity_distribution.jsonl', action='store', help='The output file containing the entity distribution over channels. It only works with either \'-edc\' or \'--entity-distribution-channel\' option. Default: entity_distribution_over_channels.json')
	
	args = parser.parse_args()

	# Add '\' character to directory paths if not present
	args.input_data_dir = args.input_data_dir if args.input_data_dir.endswith('/') else args.input_data_dir + '/'
	args.output_data_dir = args.output_data_dir if args.output_data_dir.endswith('/') else args.output_data_dir + '/'



	if not os.path.exists(args.input_data_dir):
		os.makedirs(args.input_data_dir)

	if not os.path.exists(args.output_data_dir):
		os.makedirs(args.output_data_dir)

	toolkit = TelegramToolkit(args.input_data_dir, args.output_data_dir)

	if args.resolve_entity_flag:
		toolkit.explicit_msg_entities()

	if args.create_channel_graph_flag:
		toolkit.create_channel_to_channel_graph()
		toolkit.save_channel_to_channel_graph(args.graph_name)

	if args.create_message_chain_flag:
		toolkit.create_msg_chain(args.message_chain_name)

	if args.entity_frequency_flag:
		toolkit.compute_entity_frequency(th=int(args.entity_frequency_threshold), use_type=args.entity_frequency_type, dest=args.entity_frequency_dest)

	if args.entity_frequency_channel_flag:
		toolkit.computer_entity_frequency_over_channels(th=int(args.entity_frequency_channel_threshold), use_type=args.entity_frequency_channel_type, dest=args.entity_frequency_channel_dest)


	if not (args.resolve_entity_flag or args.create_channel_graph_flag or args.create_message_chain_flag or args.entity_frequency_flag or args.entity_frequency_channel_flag):
		parser.print_help()



	
	# creation of channel to channel graph based on forwarded messages 
	#toolkit.create_channel_to_channel_graph()
	#toolkit.save_channel_to_channel_graph(CHANNEL_TO_CHANNEL_GRAPH_OUT)


	# entities explicitation
	#toolkit.explicit_msg_entities(OUTPUT_DATA_DIR)

	#channels chain
	#toolkit.create_msg_chain()



				

































