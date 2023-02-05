import argparse
from libs.example import rand_result
def main():
    
    parser = argparse.ArgumentParser(description="Bus speed and data-size")
    parser.add_argument("--data_size", type = int, required=True)
    parser.add_argument("--bus_speed",type = int,required=True)
    args = parser.parse_args()
    
    s = rand_result(args.bus_speed, args.data_size)
    print(s)
           
if __name__ == '__main__':
    main()        
         