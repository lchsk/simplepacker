import sys
import getopt

class Settings(object):
    def __init__(self):

        # parameters dictionary
        self.params = {}

        # Path to the input folder
        self.params['input'] = ''

        # Output filename
        self.params['output'] = ''

        # Size of output image (width, height)
        self.params['output_size'] = [1024, 1024]

        # if set to true, each tile will be accompanied by a txt file
        # with parameters etc for the tile
        self.params['synchronise'] = False

    def help(self):
        print 'Help...'
        sys.exit(0)

    def read_parameters(self):
        opts, args = getopt.getopt(sys.argv[1:], "Hi:o:w:h:s", ['help', 'input', 'output', 'width', 'height', 'synchronise'])

        try:
            for opt, arg in opts:
                if opt in ("-H", "--help"):
                    self.help()
                elif opt in ('-i', '--input'):
                    self.params['input'] = arg
                elif opt in ('-o', '--output'):
                    self.params['output'] = arg
                elif opt in ('-w', '--width'):
                    self.params['output_size'][0] = int(arg)
                elif opt in ('-h', '--height'):
                    self.params['output_size'][1] = int(arg)
                elif opt in ('-s', '--synchronise'):
                    self.params['synchronise'] = True
                else:
                    self.help()
            
        except getopt.GetoptError:
            self.help()

    def print_parameters(self):
        print 'Parameters:'
        for k, v in self.params.iteritems():
            print '\t' + k + ': ' + str(v)