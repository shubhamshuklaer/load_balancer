import getopt

num_tokens=10

def usage():
    print("Client usage TODO")

def generate_data_list(args):
    try:
        opts,args=getopt.getopt(args,"l:")
    except getopt.GetoptError:
        usage()
        exit(2)

    for opt,arg in opts:
        if opt=="-l":
            num_tokens=int(arg)

    print("client num_tokens: "+str(num_tokens))

    return range(num_tokens)

def accept_data(data):
    print("client: "+str(data))
