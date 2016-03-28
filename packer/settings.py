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

        # Path to the file (in info file)
        self.internal_path = ''

        # Size of output image (width, height)
        self.params['output_size'] = [1024, 1024]

        # if set to true, each tile will be accompanied by a txt file
        # with parameters etc for the tile
        self.params['synchronise'] = False

        self.params['step'] = 20

        self.params['padding'] = 5


    def help(self):
        print 'Help...'
        sys.exit(0)

    def read_parameters(self):
        opts, args = getopt.getopt(sys.argv[1:], "Hi:o:w:h:sp:S:I:", ['help', 'input', 'output', 'width', 'height', 'synchronise', 'padding', 'step', 'internal_path'])

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
                elif opt in ('-p', '--padding'):
                    self.params['padding'] = int(arg)
                elif opt in ('-S', '--step'):
                    self.params['step'] = int(arg)
                elif opt in ('-I'):
                    self.params['internal_path'] = arg

                else:
                    self.help()

        except getopt.GetoptError:
            self.help()

    def print_parameters(self):
        print 'Parameters:'
        for k, v in self.params.iteritems():
            print '\t' + k + ': ' + str(v)