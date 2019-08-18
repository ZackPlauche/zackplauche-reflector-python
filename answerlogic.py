# Reflector/reflector/answerlogic/answer_logic.py

# -*- coding: utf-8 -*-
from pathlib import Path
import re
import os
from datetime import datetime
import csv
import pandas as pd

def answer(questions, answer_type='text', output='list', **kwargs):
	'''answer(questions, answer_type='text' output='list', **kwargs)

	Creates a loop where user can answer however much text
	they would like to.

	:param *questions: Enter a question to give an answer to.
	:param answer_type: Chooese whether you'd like text answers, listed answers, or yes or no answers
	:param **kwargs: So far only lets you add indexes to your questions
	:return: pandas dataframe providing full answer information

	'''
	# Accept question or questions
	questions = question_format_check(questions)

	# List of indexes for each question
	question_indexes = list(range(1, len(questions) + 1))

	# Initialize list of answers
	answers = []

	# Collect data for dataframe
	answer_dict = {
		'Question Index': question_indexes,
		'Questions': questions,
		'Answers': answers
	}

	# Ask each question in the given list of questions
	for question in questions:

		# Container to collect each questions answer
		answer_collector = []

		# Adds a question index if question_index=True
		if kwargs.get('question_index'):
			question_index = f'({questions.index(question) + 1} out of {len(questions)})'

		# Makes all questions collect only a single response as the answer
		if answer_type == 'oneoff':

			# Ask the same one off question and build a list to return as the answer
			if kwargs.get("loop"):

				for iteration in range(1, kwargs.get("loop") + 1):
					if kwargs.get('question_index'):
						looped_oneoff_answer = input(
							f'{question} {question_index} ({iteration} of {kwargs.get("loop")}): ')
					else:
						looped_oneoff_answer = input(f'{question} ({iteration} of {kwargs.get("loop")}): ')

					answer_collector.append(looped_oneoff_answer)

			# Make all oneoff questions yes or no questions if answer_type == 'yorn'
			elif kwargs.get('yorn'):

				# Ask yes or no question with question index if question_index=True
				if kwargs.get('question_index'):
					answer = input(f'{question} {question_index} (y/n): ')

				else:
					# Ask yes or no question normally
					answer = input(f"{question} (y/n): ")

			# Ask oneoff question with a question_index
			elif kwargs.get('question_index'):
				answer = input(f'{question} {question_index}: ')

			# Ask oneoff question normally
			else:
				answer = input(f'{question}: ')


		else:

			# Add an answer counter if answer_type='listed' and ordered=True
			if answer_type == 'listed' and kwargs.get('ordered'):
				answer_counter = 1

			# Ask the question
			if kwargs.get('question_index'):

				# Ask the question displaying the index
				print(f"{question} {question_index}")

			else:
				# Ask the question normally
				print(f"{question}")

			# Loop starts to continually to collect text_answers.
			while True:

				if answer_type == 'listed':

					if kwargs.get('ordered'):

						# Prints out the answer number and allows for input
						if kwargs.get('cap'):

							# Automatically find an answer cap within each question
							if kwargs.get('cap') == 'auto':
								pattern = "\d+"
								regex = re.compile(pattern)
								match = regex.search(question)
								if match:
									answer_cap = int(match.group())
								else:
									answer_cap = False

							# Manually add an answer cap
							if type(kwargs.get('cap')) == type(int()):
								answer_cap = kwargs.get('cap')

							# If answer cap was made
							if answer_cap:
								listed_answer = input(f'{answer_counter} of {answer_cap}. ')

							# When no answer_cap is found
							else:
								listed_answer = input(f'{answer_counter}. ')


						# When there is no answer cap
						else:
							listed_answer = input(f'{answer_counter}. ')
							answer_counter += 1

					else:
						listed_answer = input(f'• ')

					# Breaks out of the loop if no answer is given.
					if listed_answer == '':
						print()
						break

					answer_collector.append(listed_answer)

					# Break out of loop after the last answer is appended if answer_counter is equal to answer_cap
					if kwargs.get('cap'):
						if answer_counter:
							if answer_counter == answer_cap:
								print()
								break

							answer_counter += 1

				elif answer_type == 'text':

					# Input the text
					text_answer = input('')

					# Exit the loop if text_answer was '.'
					if text_answer == '.':
						break

					# Adds Python formatting option.
					if kwargs.get('format') == 'python':
						# Add a line break after each answer.
						text_answer = f'{answer}\n'

					# Collect all of the text organized into a list
					answer_collector.append(text_answer)

			# Make the list into a single formatted string of text after the answer loop breaks
			if answer_type == 'listed':
				answer = answer_collector

			elif answer_type == 'text':
				answer = ' '.join(answer_collector)

		if answer_type == 'oneoff' and kwargs.get("loop"):
			answer = answer_collector

		# Add each answer to answers list
		answers.append(answer)

	# Turn answer dictionary into a pandas DataFrame
	answers_dataframe = pd.DataFrame(answer_dict)

	# return kwargs
	if output == 'list':
		if len(questions) == 1:
			return answer
		else:
			return answers
	elif output == 'dict':
		return answer_dict
	elif output == 'dataframe':
		return answers_datafarme

def activity(activity_name, questions, frequency=None, ordered=False, cap=None, **kwargs):
	'''Shorter format for added funcionality for each reflector activity.'''

	# Check questions for formatting errors
	questions = question_format_check(questions)

	# Add frequency if frequency is defined
	if frequency:
		questions = add_frequency(questions, frequency)

		# Add the frequency to the activities name
		activity_name = f'{activity_name} ({frequency})'

	# Walk through questions and collect answer data
	activity_data = answer(questions, answer_type='listed', ordered=ordered, cap=cap)

	# If kwarg "export" exists, export data as it should be exported.
	if kwargs.get('export'):
		if kwargs.get('export') == 'report':
			try:
				export(activity_name.title(), activity_data, report=kwargs.get('columns'))
			except:
				raise Exception('Must include the keyword argument of "columns" which must equal a list of columns.')
		elif kwargs.get('export') == 'date':
			export(activity_name.title(), activity_data, date=True)
		else:
			export(activity_name.title(), activity_data)

	# Return activity data
	return activity_data

def arg_check(arg_name, response_list, arg):
	if type(response_list) == str:
		appropriate_response = response_list
	else:
		appropriate_response = f'either {", ".join(response_list[:-1])} or {response_list[-1]}'

	if arg not in response_list:
		raise Exception(
			f'Arugument "{arg_name}" must equal {appropriate_response}. Please check your spelling and try again.')

def add_frequency(questions, frequency):
	'''Add frequency to a question or series of questions'''
	# Lowercase frequency to ensure proper string format is standard from the beginning
	frequency = frequency.lower()

	# arg_check on frequency
	arg_check('frequency', ['daily', 'weekly', 'monthly', 'yearly'], frequency)

	# Add a time to add to the questions
	if frequency == 'daily':
		time = 'day'
	elif frequency == 'weekly':
		time = 'week'
	elif frequency == 'monthly':
		time = 'month'
	elif frequency == 'yearly':
		time = 'year'

	# Add time to each question
	questions = [f'{question[:-1]} for the {time}?' for question in questions]

	return questions

def display(filename, keep='text', directory='Data Storage'):
	'''display(title, *list_to_display, ordered=False)

	Displays items in a basic list format.

	To display an entire list, you'll need to add a * in front of the list name.
	For example: *mylist
	Otherwise it will print the whole list.
	'''

	# Print/Display itmes first if they exist already.
	if os.path.exists(f'.\\{directory}\\{filename}'):
		file = open(f'.\\{directory}\\{filename}')
		file_text = file.read()

		# Sort all items into individual list
		title = re.compile('(.+)\:').search(file_text).group(1)
		items = re.compile('\d+\. (.+)').findall(file_text)
		print(file_text)
		file.close()

		if keep == 'file_text':
			return file_text
		if keep == 'title':
			return title
		if keep == 'items':
			return items
		if keep == 'all':
			return file_text, title, items

# TODO: Fix export not adding the title to files.
def export(filename, data, directory='Data Storage', **kwargs):
	'''Exports data into a file for storage.

	:param report: add a list of column names for your report.'''

	# Skip the whole function if data = None
	if not data or not data[0]:
		pass

	else:

		# Remove file_type from filename
		if filename[:-4] in {'.txt', '.csv'}:
			filename = filename[:-4]

		# Create the directory to store your data if it doesn't already exist.
		os.makedirs(directory, exist_ok=True)

		# Determine the type of file.
		data_type = type(data)
		if data_type == list or data_type == str:
			if data_type == str:
				data = tuple([data])
			if kwargs.get('report'):
				filetype = 'csv'
			else:
				data = tuple(data)
				filetype = 'txt'
		if data_type == pd.DataFrame:
			filetype = 'xlsx'

		# Create a text file that stores the data in a list format.
		if filetype in {'txt', 'csv'}:

			# If a file doesn't exist, write it.
			if not os.path.isfile(f'.\\{directory}\\{filename}.{filetype}') or kwargs.get('overwrite'):  # If overwrite=True, overwrite the a file.
				if filetype is 'csv':
					file = open(f'.\\{directory}\\{filename}.{filetype}', 'w', newline='')
				elif filetype is 'txt':
					file = open(f'.\\{directory}\\{filename}.{filetype}', 'w')
					print(file.mode)

			# If a file does exist, append to it.
			else:
				if filetype is 'csv':
					file = open(f'.\\{directory}\\{filename}.{filetype}', 'a+', newline='')
				elif filetype is 'txt':
					file = open(f'.\\{directory}\\{filename}.{filetype}', 'a+')

			# Create time variables csv and 'date' reports
			now = datetime.now()
			todays_date = f'{now.month}/{now.day}/{now.year}'
			today = now.strftime('%A')
			time = now.strftime("%I:%M %p").lstrip('0')

			# Write report/csv
			if filetype is 'csv':

				# Define csv writer
				writer = csv.writer(file)

				# Add time tracking columns to csv reports.
				if kwargs.get('report'):
					time_column_headers = ['Date', 'Day']
					time_column_data = [todays_date, today]
				if kwargs.get("time") == 'full':
					time_column_headers.append('Time')
					time_column_data.append(time)

				# If file is in write mode, add a header row
				if file.mode == 'w':
					writer.writerow(time_column_headers + kwargs.get('report'))

				# If the data inside of the data is a list, join each list of answers into a single answer and put it into a list
				if type(data[0]) is list:
					writer.writerow(time_column_data + [', '.join(answer) for answer in data])

				# Otherwise, join the data and add it to the report.
				else:
					if len(', '.join(data)) is len(kwargs.get('report')):
						writer.writerow(time_column_data + [', '.join(data)])
					else:
						writer.writerow(time_column_data + data)

			elif filetype is 'txt':

				# Write title of text file if file is in write mode.
				if file.mode == 'w':
					print("Adding title to .txt file...\n")
					file.write(f'{filename}:\n\n')
					print('File title added...\n')

				try:
					file.seek(0)
					last_line = file.readlines()[-1]
					last_index_regex = re.compile('(\d+).')
					last_index_match = last_index_regex.search(last_line)
					index = int(last_index_match.group(1)) + 1
				except:
					index = 1

				# Text report template
				if kwargs.get('report'):
					questions = kwargs.get('report')
					for answer, question in zip(data, questions):
						file.write(f'Question {kwargs.get("report").index(question) + 1}: {question}\n\nAnswer: {answer}')

				# List Template
				else:


					# Write date if date is not in file text
					if kwargs.get('date'):
						file.seek(0)
						try:
							filetext = file.read()
							date_match = re.compile(todays_date).search(filetext).group()
						except:
							date_match = None
						if date_match == todays_date:
							print('Date skipped')
						else:
							print('Adding Date')
							file.write(f'\n{todays_date}\n')

					print('Writing list...\n')
					for item in data:
						if item is not '':
							file.write(f'{index}. {item}\n')
							index += 1
					print('List wrote...\n')
				file.close()

def integrity(yorn_questions_list, yorn_answers, dependency=None):
	'''Takes in a list of yes or no answers and their resopnses and converts them to a total percentage value
    based on a y to n ratio.'''

	# Integrity starts at 100%
	integrity = 100

	# Each piece of the integrity is made up of the maximum integrity divided by the number of yes or no questions
	piece = 100 / len(yorn_questions_list)

	# Subtract a piece from the maximum integrity for each "no" answer
	for answer in yorn_answers:
		if answer == 'n' or answer == 'no':
			integrity -= piece

	# Put the integrity in an integer format for better readability (no messy decimals)
	integrity = f'{int(integrity)}%'

	return integrity

def list_reflector(filename, topic, question, directory='Data Storage', **kwargs):
	'''full_answer(filename, topic, questions, **kwargs)

	:param filename:
	:param topic:
	:param question:
	:param kwargs:
	:return:
	'''

	# Pulls title from filename
	title = re.compile('(.+)\.').search(filename).group(1)

	# Print/Display goals first if they exist already.
	if os.path.exists(f'.\\{directory}\\{filename}'):
		display_text, filetitle, items = display(filename, 'all')

		# Add or Rewrite new items.
		choice = pick_option(f'Would you like to add to or rewrite your {topic}?', ['add', 'rewrite', 'remove', 'no'])
		if not choice in {'no', 'n', ''}:
			if choice != 'remove':
				new_items = answer(question, answer_type='listed', ordered=True)
				if choice == 'add':
					print(f'Exporting {topic[0].upper() + topic[1:]}...\n')
					export(title, new_items)
					print(f'{topic[0].upper() + topic[1:]} exported...')
				elif choice == 'rewrite':
					export(title, new_items, overwrite=True)
			elif choice == 'remove':
				print()
				# Rewrite file without the removed number items
				item_numbers = []
				while True:
					item_number = input(f'Enter the number of {topic} you\'d like to remove (or press "enter" with nothing to end): ')
					if item_number == '':
						break
					item_numbers.append(int(item_number))
				remove_items = []
				for number in item_numbers:
					remove_items.append(items[number - 1])
				for item in remove_items:
					items.remove(item)
				export(title, items, overwrite=True)
				return items

			# Put current topic_items in a list
		else:
			regex = re.compile('.+\. (.+)')
			topic_items = regex.findall(display_text)

	# Write goals for the first time.
	else:
		topic_items = answer(question, type='listed', ordered=True)
		export(title, topic_items)

		return topic_items

def pick_option(question, acceptable_answers):

	choice = input(f'{question} ({"/".join(acceptable_answers)}): ').lower()
	print()

	# Answer validation
	if choice is not '':
		while choice not in [answer.lower() for answer in acceptable_answers]:
			print('ERROR: That is not a valid answer.\n')
			print('Please select a valid answer from this list:\n')

			for answer in acceptable_answers:
				print(f'{acceptable_answers.index(answer) + 1}. {answer}')
			print()

			choice = input('Enter the number of the option you\'d like to pick: ')
			print()
			try:
				choice = acceptable_answers[(int(choice) - 1)].lower()
			except:
				pass

			if choice in [answer.lower() for answer in acceptable_answers]:
				break

	return choice

def question_format_check(questions):
	'''Puts questions that are only a string into a single question, or if the data type is not
	a list, stirng, or tuple, it raises an exception error.

	:param questions: list or string of questions
	:return : returns a string in a tuple or a list of questions'''

	if type(questions) in (list, tuple, str):
		if type(questions) is str:
			question = tuple([questions])
			return question
		return questions
	else:
		raise Exception( ('"questions" argument must be a string, tuple, or a list.'))

def smart_choice(menu_items):
	'''
    :param menu_items: Allows user to input list of activities to do to return a choice.
    :returns : Exact item chosen through the items index.
    '''

	choice_range = f'(from {menu_items.index(menu_items[0]) + 1} to {menu_items.index(menu_items[-1]) + 1})'

	for item in menu_items:
		print(f'{menu_items.index(item) + 1}) {item}')

	choice = input(f'\nActivity number {choice_range}: ')
	print()
	if choice == '':
		pass
	else:
		try:
			if int(choice) in range(len(menu_items) + 1):
				pass
			else:
				while True:
					print("ERROR: Given Response outside the number range.\n")
					choice = input("Please enter activity number next to corresponding acivity: ")

					if int(choice) in range(len(menu_items + 1)):
						break
			choice = menu_items[int(choice) - 1]

			print('\n')
		except:
			while True:
				print("ERROR: Given response was not a number.\n")
				choice = input("Please enter activity number next to corresponding acivity: ")
				print()

				try:
					if int(choice) in range(len(menu_items)):
						pass
					else:
						while True:
							print("ERROR: Given Response outside the number range.\n")
							choice = input("Please enter activity number next to corresponding acivity: ")
							print()

							if int(choice) in range(len(menu_items)):
								break
					choice = menu_items[int(choice) - 1]
					break
				except:
					continue

				try:
					if choice in [str(menu_items.index(item) + 1) for item in menu_items]:
						choice = menu_items[int(choice) - 1]
						print()
						break
				except:
					continue
	return choice

def test():
	questions = [
		'What are your priorities?',
		'What are your wins?'
	]
	activity('test', questions, export_data=False, frequency='daily', ordered=True, cap=3)

if __name__ == '__main__':
	test()
