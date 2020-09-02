import pandas as pd
import PyCO2SYS
import argparse
import requests
import pickle



def load_merged_df(data):
    
    '''
    Finds all the required values from the merged csv file
    '''
    #downloads and saves the csv file
    r = requests.get(data)
    open('/tmp/merged.csv','wb').write(r.content)

    #read and process merged csv
    df = pd.read_csv("/tmp/merged.csv")
    processed_df = df.drop_duplicates('Bottle')
    
    #print the required 3 variables
    scraped_df = processed_df[['Bottle','T090C', 'PrDM', 'Sal00','OxsatML/L', 'Silicate', 'Phosphate', 'Ammonium']]
    print(scraped_df.head)

    

    #find the length of the df to pull out each value later on
    length = len(scraped_df)
    x = length - 1
    counter=1


    #loops through every row in the df to pull out and assign each variable
    while counter <= x:
        bottle_value = scraped_df.iat[counter,0]
        pressure_value = scraped_df.iat[counter,2]
        temp_value = scraped_df.iat[counter,1]
        sal_value = scraped_df.iat[counter,3]

        #check for dissolved oxygen value (DIC)
        if pd.isna(scraped_df.iloc[counter,4]) == True: 
            pass
        else:
            dic_value = scraped_df.iat[counter,4]

        '''
        CHECK FOR TA
        #check for TA
        if pd.isna(scraped_df.iloc[counter,4]) == True: 
            print("pass")
            pass
        else:
            dic_value = scraped_df.iat[counter,4]
            print(dic_value)
        '''


        '''
        CHECK FOR pH
        #check for pH
        if pd.isna(scraped_df.iloc[counter,4]) == True: 
            print("pass")
            pass
        else:
            dic_value = scraped_df.iat[counter,4]
            print(dic_value)
        '''
        
        '''
        CHECK FOR pCO2
        #check for pCO2
        if pd.isna(scraped_df.iloc[counter,4]) == True: 
            print("pass")
            pass
        else:
            dic_value = scraped_df.iat[counter,4]
            print(dic_value)
        '''
        
        #check for silicate
        if pd.isna(scraped_df.iloc[counter,5]) == True: 
            print("pass")
            pass
        else:
            silicate_value = scraped_df.iat[counter,5]


        #check for phosphate
        if pd.isna(scraped_df.iloc[counter,6]) == True: 
            print("pass")
            pass
        else:
            phosphate_value = scraped_df.iat[counter,6]


        #check for ammonia
        if pd.isna(scraped_df.iloc[counter,7]) == True: 
            print("pass")
            pass
        else:
            ammonia_value = scraped_df.iat[counter,7]
            print(ammonia_value)

        '''
        #check for sulfide
        if pd.isna(scraped_df.iloc[counter,7]) == True: 
            print("pass")
            pass
        else:
            ammonia_value = scraped_df.iat[counter,7]
            print(ammonia_value)
        '''
        #counter to move to next row
        counter=counter+1
    
    return(bottle_value,pressure_value,temp_value, sal_value,dic_value,ta_value,ph_value,pco2_value, silicate_value, phosphate_value, ammonia_value, sulfide_value)


def mar_carb_calc(carbonic_acid_option, bisulphate_option, pH_option, hf_diss_option, tot_borate, bottle_value, pressure_value, temp_value,
        sal_value, dic_value, ta_value, ph_value, pco2_value, silicate_value, phosphate_value, ammonia_value, sulfide_value):

    '''
    assemble and check for null values in inputs and then enter inputs into the pyCO2SYS_nd
    '''

    #create list of inputs
    value_list = [carbonic_acid_option, bisulphate_option, pH_option, hf_diss_option, tot_borate, bottle_value, pressure_value, temp_value,
        sal_value, dic_value, ta_value, ph_value, pco2_value, silicate_value, phosphate_value, ammonia_value, sulfide_value]

    #iterate through list of data and check if they are null and if they are assign them a value of None
    counter = 0
    for value in value_list:
        if pd.isna(value) == True:
            value_list[counter] = None
            counter = counter + 1

    #entering valid inputs
    PyCO2SYS.CO2SYS_nd()

def main():
    
    #parses user input
    parser = argparse.ArgumentParser()
    parser.add_argument("VAR1", type=str, default="", help= "enter an erddap endpoint") #data
    parser.add_argument("VAR2", type=int, default="", help= "choice of carbonic acid dissociation") #opt_k_carbonic
    parser.add_argument("VAR3", type=int, default="", help= "choice of potassium  sulfate dissociation constant") #opt_k_bisulphate
    parser.add_argument("VAR4", type=int, default="", help= "choice of pH scale usage") #opt_pH_scale
    parser.add_argument("VAR5", type=int, default="", help= "choice of hydrogen fluoride dissociation") #opt_k_fluoride
    parser.add_argument("VAR6", type=int, default="", help= "total borate") #opt_total_borate and ignored if total borate arg is provided 
    args = parser.parse_args()

    #assigns user input to variables
    data = args.VAR1
    carbonic_acid_option = args.VAR2
    bisulphate_option = args.VAR3
    pH_option = args.VAR4
    hf_diss_option = args.VAR5
    tot_borate = args.VAR6
    

    #function call to scrape required information from the dataset
    bottle_value, pressure_value,temp_value, sal_value,dic_value,ta_value,ph_value,pco2_value, silicate_value, phosphate_value, ammonia_value, sulfide_value = load_merged_df(data)

    #function to perform the calculation
    mar_carb_calc(carbonic_acid_option,
        bisulphate_option,pH_option,hf_diss_option,tot_borate,bottle_value,pressure_value,temp_value,
        sal_value,dic_value,ta_value,ph_value,pco2_value, silicate_value, phosphate_value, ammonia_value, sulfide_value)



if __name__ == "__main__":
    main()
