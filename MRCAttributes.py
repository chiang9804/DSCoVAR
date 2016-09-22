class MRCAttributes(object):
    def findMRCAttributes(self, word, mrc_dictionary):
        if word in mrc_dictionary:
            return mrc_dictionary[word]
        else:
            return None

    def readMRCData(self, filename):
        # word, MRC_NLET, MRC_NPHM, MRC_NSYL, MRC_KFFRQ, MRC_TLFRG, MRC_BFRQ, MRC_FAM, MRC_CNC, MRC_IMG, MRC_AOA
        mrc_dictionary = {}
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            headers = reader.next()
            for row in reader:
                (word, MRC_NLET, MRC_NPHM, MRC_NSYL, MRC_KFFRQ, MRC_TLFRG, MRC_BFRQ, MRC_FAM, MRC_CNC, MRC_IMG, MRC_AOA) = row[:11]
                word = word.strip() # There is ending space in each word
                if word not in mrc_dictionary:
                    mrc_dictionary[word] = {"MRC_NLET" : MRC_NLET, \
                                            "MRC_NPHM" : MRC_NPHM, \
                                            "MRC_NSYL" : MRC_NSYL, \
                                            "MRC_KFFRQ" : MRC_KFFRQ, \
                                            "MRC_TLFRG" : MRC_TLFRG, \
                                            "MRC_BFRQ" : MRC_BFRQ, \
                                            "MRC_FAM" : MRC_FAM, \
                                            "MRC_CNC" : MRC_CNC, \
                                            "MRC_IMG" : MRC_IMG, \
                                            "MRC_AOA" : MRC_AOA}
        return mrc_dictionary
    
    def addMRCAttributesToWordList(self, word_list_filename, mrc_dictionary, out_filename, DEBUG):
        #df = pd.read_csv(word_list_filename)
        #for word in df.targ:
        #    df.loc[word] = pd.Series(mrc_dictionary[word])
        word_list = []
        with open(word_list_filename, 'rb') as f:
            reader = csv.reader(f)
            headers = reader.next()
            if DEBUG:
                for row in reader:
                    (_, _, _, _, _, _, _, target) = row[:8]
                    if target in mrc_dictionary:
                        print target, mrc_dictionary[target]
                    else:
                        print target, None

            else:
                with open(out_filename, 'wb') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['word'] + mrc_dictionary[next(mrc_dictionary.__iter__())].keys())
                    for row in reader:
                        (_, _, _, _, _, _, _, target) = row[:8]
                        if target in mrc_dictionary:
                            writer.writerow([target] + mrc_dictionary[target].values())
                        else:
                            writer.writerow([target])



import csv
import getopt, sys
#import pandas as pd

def usage():
    print 'Usage: '+sys.argv[0]+' [-i <input_file>][-o <output_file>][-W <words_file>][-w test_word1 test_word2 ...]'

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hi:o:tbpms:W:w', ['help', 'input=', 'output=', 'words_list='])
        if not opts:
            print 'No options supplied'
            usage()
    except getopt.GetoptError,e:
        print e
        usage()
        sys.exit(2)
    
    in_filename = None
    out_filename = None
    test_words = None
    word_list_filename = None
    DEBUG = 0
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-i', '--input'):
            in_filename = arg
        elif opt in ('-w'):
            test_words = args
        elif opt in ('-W', '--word_list'):
            word_list_filename = arg
        elif opt in ('-o', '--output'):
            out_filename = arg
    
    # Check input file
    if in_filename == None:
        in_filename = "mrc_dictionary.csv"
    try:
        in_file = open("mrc_dictionary.csv", "r")
    except:
        usage()
        sys.exit("ERROR. Can't read the input file "+in_filename+".")
    in_file.close()
	
    if out_filename == None:
        DEBUG = 1
    
    # TODO: need to handle error.
    mrc_dictionary = MRCAttributes().readMRCData('mrc_dictionary.csv')
    
    if test_words:
        for test_word in test_words:
            print "The MRC attributes for word: ", test_word
            print MRCAttributes().findMRCAttributes(test_word, mrc_dictionary)
        sys.exit()
    elif word_list_filename == None:
        usage()
        sys.exit("Should have either test_words or words_list as input.")
	
    try:
        word_file = open(word_list_filename, "r")
    except:
        sys.exit("ERROR. Can't read the word_list file "+word_list_filename+".")
    word_file.close()
    
	# TODO: need to handle error.
    MRCAttributes().addMRCAttributesToWordList(word_list_filename, mrc_dictionary, out_filename, DEBUG)




if __name__ == '__main__':
    main(sys.argv[1:])
