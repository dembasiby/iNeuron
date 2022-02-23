import sqlite3
import logging
import os
import re

logging.basicConfig(filename='sqlite3ass1.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class FileParser:
    
    @classmethod
    def word_counter(cls, words:'file name or list of names'):
        """
        Input: A file or a list of names
        Output: Return a list of tuples including distinct words in 
        a list and the number of times each word is repeated 
        in the list
        """
        
        try:
            os.path.isfile(words)
            words = FileParser.clean_file(words)
        except: pass
        
        try:
            words_object = {}
            for word in words:
                if word in words_object:
                    words_object[word] += 1
                else:
                    words_object[word] = 1
            tuple_list = [ (word, count) for word, count in words_object.items() ]
            logging.info('List of tuples created from the list provided')
            return tuple_list
        except Exception as e:
            logging.error(e)
    
    @classmethod
    def word_group_counter(cls, words: 'file or list of words'):
        """
        Input: A file or a list of words
        Output: Return a list of tuples of letters and count
        of each letters found as first letter of a 
        word in the list.
        """
        try:
            os.path.isfile(words)
            words = FileParser.clean_file(words)
        except: pass
        
        try:
            first_letters = set([ e[0] for e in words ])
            first_letters_list = [ e[0] for e in words]
            words_grouped_by_starting_letter = FileParser.__get_count(
                first_letters, first_letters_list)
            logging.info('List of tuples of letters and count of words created')
            return words_grouped_by_starting_letter
        except Exception as e:
            logging.error(e)
        
    @classmethod
    def clean_file(cls, filename: 'File path'):
        """
        Input: a file/filepath containing a list of
        words/characters. The words may contain unwanted
        characters like numbers of special characters
        Output: Return a list of words purged of all 
        non-alphabetical characters.
        """
        try:
            content_list = []
            with open(filename, 'r') as f:
                for line in f.readlines():
                    new_content = re.sub('[^a-zA-Z]+', '', line)
                    if new_content != '\n' and new_content:
                        content_list.append(new_content)
            logging.info('List purged of non alphabetical characters')
            return content_list
        except Exception as e:
            logging.error(e)
    
    @classmethod
    def files_to_tuplelist(cls, *files: 'list of file names/paths'):
        """
        Input: one or many text files including list of words
        Output: a blended list of tuples including unique
        words and the count of each word in the blended list.
        The initial files are cleaned first before merged into 
        one big list.
        """
        try:
            if len(files) < 1:
                raise InputError('Should take at least one file...')
            main_list = []
            for file in files:
                main_list += FileParser.clean_file(file)

            return FileParser.word_counter(main_list)
        except Exception as e:
            logging.error(e)
            
    @classmethod
    def __get_count(cls, unique_elements_list, raw_list):
        """
        Input: unique elements to count and a raw list
        Output: list of tuples including unique
        words and the count of each word in the raw list. 
        """
        try:
            return [ (e, raw_list.count(e)) for e in unique_elements_list ]
        except Exception as e:
            logging.error(e)
            
    @classmethod
    def save_to_db(cls, 
                   db: 'database connection object', 
                   tablename: 'database table name', 
                   tuplelist: list):
        """
        Input: a database connection object, a db table name, and 
        a list of tuples including a word and the count of that word.
        Output: None. The method insert the provided list to database.
        """
        try:
            c = db.cursor()
            for word, count in tuplelist:
                c.execute(f'INSERT INTO {tablename} VALUES ("{word}", "{count}")')
            db.commit()
            logging.info('Content of tuple list saved in database.')
        except Exception as e:
            logging.error(e)
        
if __name__ == '__main__':
    FileParser()