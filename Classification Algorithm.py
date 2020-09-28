#!/usr/bin/python
# Author: Varnit Tewari
# 

import matplotlib.pyplot as plt
import math
import sys

# Object that takes data file as an input and does all the necessary 
# operations. A working example of finding the best threshold using classification.
class Classifier:

    # contructor method
    # used to create the object and pass the necessary input arguments
    def __init__(self,data_file):
        self.data_file = data_file              # data  file we are going to use
        self.data_to_use = 0                    
        self.height_data_to_quantize = 0        # used for quantization
        self.age_data_to_quantize = 0           # used for quantization
        self.target_variable_data = 0           # used to store the class values

    # This nethod is made to read the abominable data 
    # It reads each line in the data file, removes the column header after
    # knowing what column number age, height ad class are present in.
    # Stores all the data in four arrays that we later use in the code
    # Converts all the string vales to float
    def read_data(self):

        data_open_file = open(self.data_file,"r")       #opens the file
        # default values for each column for this file
        age_column = 0                      
        height_column = 1
        class_column = 7
        self.data_to_use = data_open_file.read().splitlines()       # reads the lines
        first_line = self.data_to_use[0]
        first_line = first_line.split(",")                  # splits the line separated by comma
        for word_idx in range(0,len(first_line)):
            character = first_line[word_idx].strip()       # checks for white spaces
            if character == "Age":                 # checks for age column
                age_column = word_idx
            elif character == "Height":             # checks for hight column
                height_column = word_idx
            elif character == "Class":              # checks for the class column
                class_column = word_idx
        
        self.data_to_use = self.data_to_use[1:]         # Removes the header

        # initializing our global variables
        self.height_data_to_quantize = [0] * len(self.data_to_use)
        self.age_data_to_quantize = [0] * len(self.data_to_use)
        self.target_variable_data = [0] * len(self.data_to_use)

        # starts storing the data
        for data_idx in range(0,len(self.data_to_use)):         
            data = self.data_to_use[data_idx].split(',')
            self.data_to_use[data_idx] = data[age_column]        # records only the age
            self.age_data_to_quantize[data_idx] = data[age_column]
            self.height_data_to_quantize[data_idx] = data[height_column] # records the height
            self.target_variable_data[data_idx] = data[class_column]
    
        self.data_to_use = [float(i) for i in self.data_to_use]     # converts string to float
        self.age_data_to_quantize = [float(i) for i in self.age_data_to_quantize]     # converts string to float
        self.height_data_to_quantize = [float(i) for i in self.height_data_to_quantize]     # converts string to float

        data_open_file.close()                  # closes the file


    # This method is used to quantize the data in the abominable data file.
    # It is mainly used for NOISE Reduction
    # passed_data = data we want to quantize
    # bin_size = the size of the bin we want to quantize the data in
    def floor_quantize(self, passed_data, bin_size):            
        data_sample = passed_data         # deep copy
        for sample_idx in range(0,len(passed_data)):           
            # fomula to quantize the data
            # we are using the floor method
            data_sample[sample_idx] = math.floor(passed_data[sample_idx]/bin_size) * bin_size
        return data_sample

    
    # This is where the main classification algorithm is implemented.
    # The first step is to quantize the data. 
    # For all thresholds, we compute four variables, i.e., false_negative, false_positive,
    # true_negative and true_positive.
    # Later false_negative and false_positive are used to find the cost function which we have
    # to minimize. For the minimum cost function, we record the best threshold and use that
    # threshold for classification.
    # data_to_quantize: the data we are going to use
    # bin_size: bin size for quantization purposes
    # if_age: parameter used to determine if we are classifying take age as the attribute or height
    #           1: for age
    #           0: for height
    def classification_algorithm(self, data_to_quantize, bin_size, if_age):

        quantized_data = self.floor_quantize(data_to_quantize, bin_size)  # get the quantized data

        # initializing a bunch of variables
        best_cost_function = float('inf')  
        best_threshold = best_idx = idx = 0        
        cost_function_array = [0] * len(quantized_data)         # used to plot the curve later
        false_alarm_rate = true_positive_rate = [0]*len(quantized_data)     # used to plot the ROC curve
        false_positive = true_positive = cost_function = 0
        num_left = num_right = 0
        num_assam = num_bhuttan = 0

        # for every threshold value, we try classifiying to determine the best threshold
        # since we do not know what side our target variable will be present, we try finding the
        # four variables for each side. One time we assume that our target variable Bhuttan is on the right
        # and the other time on the left.
        # Then we compare the cost functions for both of them and use the one that is minimum.
        for threshold in quantized_data:
            # initializing all four variables for each side -left and right
            true_negative_left = true_positive_left = false_negative_left = false_positive_left = 0
            true_negative_right = true_positive_right = false_negative_right = false_positive_right = 0

            # number present on each side
            num_bhuttan_left = num_assam_left = 0
            num_bhuttan_right = num_assam_right = 0

            # here, we assume target variable is on the right side
            for data_idx in range(0,len(quantized_data)):
                if quantized_data[data_idx] <= threshold:   # we assume the actual situation to be negative here
                    if self.target_variable_data[data_idx] == "Bhuttan":
                        # since we got our target variable here, we think it is a false negative
                        # suspected situation is not same as actual situation
                        false_negative_right +=1            
                        num_bhuttan_right +=1
                    else:
                        # we do not find our target variable, this means it is a true negative
                        # suspected situation is same as actual situation
                        true_negative_right +=1
                        num_assam_right +=1
                else:                                  # we assume the actual situation to be positive here
                    if self.target_variable_data[data_idx] == "Bhuttan":
                        # since we got our target variable here, this means it is a true positive
                        # suspected situation is same as actual situation
                        true_positive_right +=1
                        num_bhuttan_right +=1
                    else:
                        # we do not find our target variable, this means it is a true negative
                        # suspected situation is not same as actual situation
                        false_positive_right +=1
                        num_assam_right +=1

            # the usual cost function formula for classification
            cost_function_right = false_negative_right + false_positive_right

            # here we assume our target variable is on the left side
            for data_idx in range(0,len(quantized_data)):
                if quantized_data[data_idx] > threshold:         # we assume the actual situation to be negative here
                    if self.target_variable_data[data_idx] == "Bhuttan":
                        # since we got our target variable here, we think it is a false negative
                        # suspected situation is not same as actual situation
                        false_negative_left +=1
                        num_bhuttan_left +=1
                    else:
                        # we do not find our target variable, this means it is a true negative
                        # suspected situation is same as actual situation
                        true_negative_left +=1
                        num_assam_left +=1
                else:                                   # we assume the actual situation to be positive here
                    if self.target_variable_data[data_idx] == "Bhuttan":
                        # since we got our target variable here, this means it is a true positive
                        # suspected situation is same as actual situation
                        true_positive_left +=1
                        num_bhuttan_left +=1
                    else:
                        # we do not find our target variable, this means it is a true negative
                        # suspected situation is not same as actual situation
                        false_positive_left +=1
                        num_assam_left +=1
            cost_function_left = false_negative_left + false_positive_left

            # here, we check for the minimum cost function and if target variable is better on left or right
            if cost_function_left < cost_function_right:
                cost_function = cost_function_left
                false_positive = false_positive_left
                true_positive = true_positive_left
                num_assam = num_assam_left
                num_bhuttan = num_bhuttan_left
                num_left +=1
            else:
                cost_function = cost_function_right
                false_positive = false_positive_right
                true_positive = true_positive_right
                num_assam = num_assam_right
                num_bhuttan = num_bhuttan_right
                num_right +=1

            # storing cost function into an array to plot the curve later
            cost_function_array[idx] = cost_function 

            # storing the minimum cost function and the best threshold
            if cost_function <= best_cost_function:
                best_cost_function = cost_function
                best_threshold = threshold
                best_idx = idx

            # these two variables are used to plot the ROC curves
            false_alarm_rate[idx] = false_positive/num_assam
            true_positive_rate[idx] = true_positive/num_bhuttan
            idx +=1

        # checking if age is being used as the attribute or height
        if if_age == 1:
            print("Best threshold for age: ", best_threshold)
            print("Cost function for age: ", best_cost_function)
        else:
            print("Best threshold for height: ", best_threshold)
            print("Cost function for height: ", best_cost_function)

        # then we graph the cos function against quantized age
        self.graph_mixed_variance(quantized_data,cost_function_array, false_alarm_rate,true_positive_rate, if_age)

        # returning a tuple with the best threshold and the side where the target variable is present
        # the side of the target variable is important to know for training and validation purposes
        if (num_left<num_right):
            return best_threshold,"right"
        return best_threshold,"left"

    # a method created to plot the curves like the scatter plot between cost function and quantized age
    # and roc curves
    # quantized_data: x axis for scatter plot
    # cost_function_array: y axis for scatter plot
    # false_alarm_rate: x axis for ROC curve
    # true_positive_rate: y axis for ROC curve
    # if_age: 1 if age is the attribute
    #         0 if height is the attribute
    def graph_mixed_variance(self,quantized_data,cost_function_array,false_alarm_rate,true_positive_rate, if_age):

        # initialzing a figure and two subplots in that figure
        fig, (ax1, ax2) = plt.subplots(1,2, figsize = (12,4))

        # first plot is the scatter plot between cost function and quantized age
        ax1.scatter(quantized_data, cost_function_array, color= "red",  marker= "*")
        # conditions to print the title of the curve and its axis titles
        if if_age==1:
            ax1.set_title('Cost Function vs Quantized Age')  # setting the title
            ax1.set_xlabel("Quantized Age")                 # setting the x axis title
        else:
            ax1.set_title('Cost Function vs Quantized Height')     
            ax1.set_xlabel("Quantized Height")
        ax1.set_ylabel("Cost Function")                     # setting the y axis title

        # second plot is the line ROC curve
        ax2.plot(false_alarm_rate, true_positive_rate, marker = 'o')
        if if_age==1:
            ax2.set_title('ROC when using Age for Best Threshold')
        else:
            ax2.set_title('ROC when using height for Best Threshold')
        ax2.set_xlabel("False alarm rate")
        ax2.set_ylabel("True Positive Rate")

        plt.show()              # shows the plots

    

    # main function that drives the whole code.
    # Its sole purpose is to call the functions 
    def main(self):
        self.read_data()
        best_threshold, target_side = self.classification_algorithm(self.height_data_to_quantize,5,0)
        best_threshold, target_side = self.classification_algorithm(self.age_data_to_quantize, 2,1)


# object creation passing the name of the data file
# prameters : name of the data file to read
fictional = Classifier(sys.argv[1])
fictional.main()