# Author: Varnit Tewari
# Homework 2
# 

import matplotlib.pyplot as plt
import numpy as np
import statistics as stt
import math

# Object that takes data file as an input and does all the necessary 
# operations  
class Otsu:

    #contructor method
    def __init__(self,data_file,alpha):
        self.data_file = data_file
        self.alpha = alpha
        self.data_to_use = 0

    
    # This method was made to read the Mystery data and store its contents
    # in a variable
    def read_data(self):
        data_open_file = open(self.data_file,"r")       # opens the file
        self.data_to_use = data_open_file.read().splitlines()       # reads the lines
        self.data_to_use = self.data_to_use[1:]         # removes the header
        data_open_file.close()              # closes the file


    # This nethod is made to read the abominable data and is very similar to 
    # read_data and has more functionalities to accomodate for reading the abominable data.
    def read_abominable_data(self):
        data_open_file = open(self.data_file,"r")       #opens the file
        self.data_to_use = data_open_file.read().splitlines()       # reads the lines
        self.data_to_use = self.data_to_use[1:]         # Removes the header
        for data_idx in range(0,len(self.data_to_use)):         
            data = self.data_to_use[data_idx].split(',')
            self.data_to_use[data_idx] = data[0]        # records only the age and not the height
        self.data_to_use = [float(i) for i in self.data_to_use]     # converts string to float
        data_open_file.close()                  # closes the file


    # This method qis used to quantize the data in the abominable data file
    def floor_quantize(self):
        BIN_SIZE_FOR_AGE = 2            
        data_sample = self.data_to_use          # deep copy
        for sample_idx in range(0,len(self.data_to_use)):           
            # fomula to quantize the data
            # we are using the floor method
            data_sample[sample_idx] = math.floor(self.data_to_use[sample_idx]/BIN_SIZE_FOR_AGE) * BIN_SIZE_FOR_AGE
        return data_sample

    
    # This is where the main Otsu method is implemented. First it initializes a few
    # variables we are going to use.
    # Then for each threshold, it finds the mixed_variance and the best threshold
    # Later, it adds the regularization part to minimize the new cost function and
    # find the new threshold
    def otsu_algorithm(self):
        np.seterr(all='ignore')
        norm_factor = 100
        quantized_data = self.floor_quantize()  # get the quantized data
        best_cost_function = float('inf')  
        best_mixed_variance = float('inf')
        quantized_data = np.array(quantized_data)       # converting quantized data into a numpy array
        MAX_THRESHOLD = np.max(quantized_data)          
        ties = 0                                # I used this to find the number of ties in the threshold
        mixed_variance_array = []               # used to graph the plot later

        for threshold in quantized_data:
            # fraction of all points less than or equal to threshold
            wt_left = (np.count_nonzero(quantized_data<=threshold))/len(quantized_data)
            # fraction of all points more than threshold
            wt_right = (np.count_nonzero(quantized_data>threshold))/len(quantized_data)
            # variance of all points less than or equal to threshold
            var_left = np.var(quantized_data[quantized_data<=threshold])
            # variance of all points greater than the threshold
            var_right = np.var(quantized_data[quantized_data>threshold])

            #finds the mixed variance here
            mixed_variance = (wt_left*var_left)+(wt_right*var_right)
            mixed_variance_array.append(mixed_variance)

            # checks for the minimum mixed_variance and best threshold
            if mixed_variance < best_mixed_variance:
                best_mixed_variance = mixed_variance
                best_threshold = threshold

            # this part was used to find the number of ties and we did not 
            # need it in the output so I commented it out
            #if mixed_variance == best_mixed_variance:
            #    print("Break the tie")
            #    ties +=1

            # Regularizations Begins
            regular_left = np.count_nonzero(quantized_data<=threshold) # all data points less than threshold
            regular_right = np.count_nonzero(quantized_data>threshold) # all data points higher than threshold
            
            # Regularization formula
            regularization = self.alpha * abs(regular_left-regular_right)/norm_factor

            # Calculating the cost function here
            cost_function = mixed_variance + regularization

            # Finding the best cost_function and threshold with regularization
            if cost_function < best_cost_function:
                best_cost_function = cost_function
                regular_best_threshold = threshold

        print("\n")
        print("Best Mixed Variance:", best_mixed_variance)
        print("Alpha:", self.alpha)
        print("Best Threshold Without Regularization: ", best_threshold)
        print("Best Threshold With Regularization: ", regular_best_threshold)

        # then we graph the mixed variance against quantized age
        self.graph_mixed_variance(quantized_data,mixed_variance_array, best_threshold, best_mixed_variance)

    # a method created to plot the curve between mixed variance and the quantized age
    # we plot a scatter plot
    def graph_mixed_variance(self,quantized_data,mixed_variance_array,best_threshold,best_mixed_variance):
        # plotting points as a scatter plot 
        plt.scatter(quantized_data, mixed_variance_array, label= "mixed variance", color= "red",  marker= "*", s=30) 
  
        # x-axis label 
        plt.xlabel('Quantized Age') 
        # y-axis label 
        plt.ylabel('Mixed Variance') 
        # plot title 
        plt.title('Mixed Variance vs Quantized Age') 
        # showing legend 
        plt.legend() 
        # making a circle to show the value used to segment the data
        plt.scatter(best_threshold ,best_mixed_variance, s=200, facecolors='none', edgecolors='b')
        # function to show the plot 
        plt.show() 


    # first method created to finish the first task of the homework which was to 
    # find the average and standard deviation of the data in the Mystery_Data_2195.csv
    def compute_avg_and_std_deviation(self):
        #self.data_to_use = [int(i) for i in self.data_to_use] 
        print("Average with All Elements:", np.mean(self.data_to_use))
        print("Standard Deviation for All Elements:", np.std(self.data_to_use))

        new_data_removed = self.data_to_use[:len(self.data_to_use)-1] # removes the last entry in the data
        print("Average with Last element removed:", np.mean(new_data_removed))
        print("Standard Deviation with last element removed:", np.std(new_data_removed))
        print ("\n")


    # main function that drives the whole code.
    # Its sole purpose is to call the functions 
    def main(self):
        #self.read_data()
        self.read_abominable_data()
        self.compute_avg_and_std_deviation()
        self.otsu_algorithm()


# object creation passing the name of the data file and alpha
# prameters : name of the data file and alpha
otsu = Otsu("Abominable_Data_For_Clustering__v44.csv", 1)
# otsu = Otsu("Mystery_Data_2195.csv", 100)
otsu.main()