import pandas as pd
import os

def convert_tuple(val):
    if isinstance(val, tuple):
        return val[0]
    else:
        return val
     

# Define a function to automate the conversion
def convert_excel_to_csv(file_path, output_path):

    print(f"Processing {file_path}")
    
    # Define the output data structure
    output_data = []
    
    idx_q = {
        1 : 3,
        2 : 5,
        3 : 7,
        'qq' : 9,
        'yy' : 11
    }

    # Read the Excel file
    excel_data = pd.ExcelFile(file_path)

    # Loop through each sheet in the Excel file
    for sheet_name in excel_data.sheet_names:

        # If it's a relevant sheet
        # if sheet_name in ['Institutional Securities', 'Wealth Management', 'Investment Management']:
        if sheet_name in ['Institutional Securities']:
            
            # print(sheet_name)  
            df = pd.read_excel(excel_data, sheet_name=sheet_name)

            q_row = False
            under_row = False
            for index, row in df.iterrows():
                
                # remove spaces
                stripped_data = row.astype(str).str.strip() 

                # Find the quarter title
                #######################################################################################
                values_to_check = ["Quarter Ended"]
                if stripped_data.isin(values_to_check).any():
                    # print(row)
                    q_row = True
                    continue
                    
                # If this is the quarters row
                #######################################################################################
                if q_row:
                    # print(row)
                    # print(row.iloc[idx_q1])
                    # print(row.iloc[idx_q2])
                    # print(row.iloc[idx_q3])

                    quarters = {
                        1 : row.iloc[idx_q[1]],
                        2 : row.iloc[idx_q[2]],
                        3 : row.iloc[idx_q[3]],
                    }
                    
                    q_row = False
                    continue

                # Find Advisory:
                #######################################################################################
                values_to_check = ["Advisory"]
                if stripped_data.isin(values_to_check).any():
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'revenue',
                            'entry_category' : 'Investment banking',
                            'entry_sub_category' : 'Advisory',
                            'entry_dollar_amount' : row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)

                        # The next rows will be for underwriting
                        under_row = True
                        continue

                # Find Underwriting - Equity:
                #######################################################################################
                values_to_check = ["Equity"]
                if stripped_data.isin(values_to_check).any() and under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'revenue',
                            'entry_category' : 'Investment banking',
                            'entry_sub_category' : 'Underwriting - Equity',
                            'entry_dollar_amount' : row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue

                # Find Underwriting - Fixed income:
                #######################################################################################
                values_to_check = ["Fixed income"]
                
                if stripped_data.isin(values_to_check).any() and under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'revenue',
                            'entry_category' : 'Investment banking',
                            'entry_sub_category' : 'Underwriting - Fixed income',
                            'entry_dollar_amount' : row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    under_row = False
                    continue

                # Find Equity:
                #######################################################################################
                values_to_check = ["Equity"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'revenue',
                            'entry_category' : 'Equity',
                            'entry_sub_category' : '',
                            'entry_dollar_amount' : row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue


                # Find Fixed income:
                #######################################################################################
                values_to_check = ["Fixed income"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'revenue',
                            'entry_category' : 'Fixed income',
                            'entry_sub_category' : '',
                            'entry_dollar_amount' : row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue

                # Find Other:
                #######################################################################################
                values_to_check = ["Other"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'revenue',
                            'entry_category' : 'Other',
                            'entry_sub_category' : '',
                            'entry_dollar_amount' : row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue

                # Find Provision for credit losses:
                #######################################################################################
                values_to_check = ["Provision for credit losses"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'expense',
                            'entry_category' : 'Provision for credit losses',
                            'entry_sub_category' : '',
                            'entry_dollar_amount' : -row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue

                # Find Compensation and benefits :
                #######################################################################################
                values_to_check = ["Compensation and benefits"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'expense',
                            'entry_category' : 'Non-interest expenses',
                            'entry_sub_category' : 'Compensation and benefits',
                            'entry_dollar_amount' : -row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue

                # Find Non-compensation expenses :
                #######################################################################################
                values_to_check = ["Non-compensation expenses"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'expense',
                            'entry_category' : 'Non-interest expenses',
                            'entry_sub_category' : 'Non-compensation expenses',
                            'entry_dollar_amount' : -row.iloc[idx_q[n]],
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # These values are only for the first row
                        if i == 0:
                            row_data['qq_amount'] = row.iloc[idx_q['qq']],
                            row_data['yy_amount'] = row.iloc[idx_q['yy']]
                            row_data['qq_amount'] = convert_tuple(row_data['qq_amount'])
                            row_data['yy_amount'] = convert_tuple(row_data['yy_amount'])
                            
                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)
                    continue

                # Find Income before provision for income taxes:
                #######################################################################################
                values_to_check = ["Income before provision for income taxes", "Income before taxes"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    income = {
                        1 : row.iloc[idx_q[1]],
                        2 : row.iloc[idx_q[2]],
                        3 : row.iloc[idx_q[3]]
                    }

                # Find Net income applicable to Morgan Stanley:
                #######################################################################################
                values_to_check = ["Net income applicable to Morgan Stanley"]
                if stripped_data.isin(values_to_check).any() and not under_row:
                    net_income = {
                        1 : row.iloc[idx_q[1]],
                        2 : row.iloc[idx_q[2]],
                        3 : row.iloc[idx_q[3]]
                    }

                    # Compute taxes
                    #######################################################################################
                    for i in range(3):
                        n = i+1
                        row_data = {
                            'segment' : sheet_name,
                            'quarter_ended' : quarters[n],
                            'metric' : 'expense',
                            'entry_category' : 'Provision for income taxes',
                            'entry_sub_category' : '',
                            'entry_dollar_amount' : -(income[n] - net_income[n]),
                            'qq_amount' : '',
                            'yy_amount' : ''
                        }

                        # Add it to the output
                        row_data_list = list(row_data.values())
                        output_data.append(row_data_list)

    # Convert the output data to a DataFrame
    output_df = pd.DataFrame(output_data, columns=[
        "segment", "quarter_ended", "metric", "entry_category", "entry_sub_category", "entry_dollar_amount", 
        "quarter_to_quarter_percent_change", "year_to_year_percent_change"
    ])
    
    # Save to CSV
    output_df.to_csv(output_path, mode="a", index=False, header=False)
    print(f"Data successfully converted and saved for {file_path}")

    return True

# Process all Excel files
import os

# Specify the folder path
folder_path = r"C:\Users\User\repos\work\excel"

# List all files in the folder
files = os.listdir(folder_path)
# print("Files in the folder:", files)

for file in files:
    # print(file)
    file_path = f"{folder_path}\\{file}"
    # print(file_path)
    convert_excel_to_csv(file_path, "finsup_all.csv")
    
print("All done")
