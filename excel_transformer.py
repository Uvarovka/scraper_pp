
csv_file = 'res_cli.csv'
data_frame = pd.read_csv(csv_file, delimiter=';')
column_data = data_frame.iloc[:, 1]
excel_file = 'number_output.xlsx'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
column_data.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
