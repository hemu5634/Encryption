import heapq
import os
class BinaryTreeNode:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.left=None
        self.right=None
        
        
    def __lt__(self,other):
        return self.freq < other.freq
    
    def __eq__(self,other):
        return self.freq == other.freq


class Huffman:
    def __init__(self,path):
        self.path=path
        self.__heap=[] 
        self.__code={}
        self.__reverseCode={}
        
    
    def frequency_dict(self,txt):
        d={}
        for ele in txt:
            if ele not in d:
                d[ele]=0
            d[ele]+=1
        return d
    
    
    def __build_heap(self,d):
        for key in d:
            frequency=d[key]
            node=BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,node)
            
    
    def __build_tree(self):
        while len(self.__heap) > 1:
            node1=heapq.heappop(self.__heap)
            node2=heapq.heappop(self.__heap)
            newFreq=node1.freq+node2.freq
            newNode=BinaryTreeNode(None,newFreq)
            newNode.left=node1
            newNode.right=node2
            heapq.heappush(self.__heap,newNode)
            
        return
    
    def __build_codes_helper(self,root,curr_bits):
        if root is None :
            return
        if root.value is not None :
            self.__code[root.value]=curr_bits
            self.__reverseCode[curr_bits]=root.value
            return
        self.__build_codes_helper(root.left,curr_bits+'0')
        self.__build_codes_helper(root.right,curr_bits+'1')
        
        
    def __build_codes(self):
        root=heapq.heappop(self.__heap)
        self.__build_codes_helper(root,'')
    
    def __build_encoded_text(self,txt):
        encoded_text=''
        for ele in txt:
            encoded_text+=self.__code[ele]
        
        return encoded_text
    
    
    def __buildPadded(self,text):
        paddedamount=8-(len(text)%8)
        for i in range(paddedamount):
            text+='0'
        padded_info="{0:08b}".format(paddedamount)
        encoded_text=padded_info + text
        
        return encoded_text
    
    def __getBytesArray(self,text):
        arr=[]
        for i in range(0,len(text),8):
            byte=text[i:i+8]
            arr.append(int(byte,2))
        return arr
    
    def compress(self):
        
        # get file from path
        file_name,file_extension = os.path.splitext(self.path)
        output_path = file_name + '.bin'
        
        # read file from path
        with open(self.path,'r+') as file , open(output_path,'wb') as output:
            text=file.read()
            text=text.rstrip()
            
            #construct frequency table of text file
            freq_dict=self.frequency_dict(text)

            #construct heap of frequency table
            self.__build_heap(freq_dict)

            #construct Binary Tree of heap
            self.__build_tree()

            #create code from Binary Tree
            self.__build_codes()

            #create encoded text
            encoded_text=self.__build_encoded_text(text)

            #padding the encoded text
            paddedEncodedText=self.__buildPadded(encoded_text)

            #getting bytes array
            bytes_array=self.__getBytesArray(paddedEncodedText)
            final_bytes=bytes(bytes_array)

            #put encoded text to binary file
            output.write(final_bytes)
        print("compressed")
        return output_path
    
    def __removePadding(self,text):
        padding=int(text[:8],2)
        text=text[8:]
        actual=text[:-1*padding]
        return actual
    
    def __decode(self,text):
        decodedstr=''
        bits=''
        for bit in text:
            bits+=bit
            if bits in self.__reverseCode:
                decodedstr+=self.__reverseCode[bits]
                bits=''
        return decodedstr
    
    def decompress(self,input_path):
        file_name,file_extension = os.path.splitext(self.path)
        output_path = file_name + '_decompressed'+'.txt'
        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bitsstring=''
            byte=file.read(1)
            while byte :
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bitsstring+=bits
                byte=file.read(1)
            actual_text = self.__removePadding(bitsstring)
            decompressed_text = self.__decode(actual_text)
            output.write(decompressed_text)
            print('decompressed')
