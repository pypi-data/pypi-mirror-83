import pandas as pd
import json
import re

dataframes = {}

def strip_dots(s):
    res = re.sub(r"^[\.]*",'',s)
    return res

def splatter3(data,keywords,parent_id="None",parent_class="None",item_name="",parent_relational="",parent_relational_id="None"):
    #print(f"//{parent_class},  {parent_relational}, {data}")
    #if the data sent to the function is a list
    parent_class = strip_dots(parent_class)
    parent_relational = strip_dots(parent_relational)
    if type(data) is list:
        #loop through the items in the list and call the function in a recursive manner
        for item in data:
            splatter3(item,parent_class=parent_class,parent_id=parent_id,item_name=item_name,parent_relational=parent_relational
                ,parent_relational_id=parent_relational_id,keywords=keywords)
    #if the data sent to the function is a dict
    elif type(data) is dict:
        this_parent_name = parent_class.split('.')[-1]
        if this_parent_name in keywords.keys():
            _id = data.get(keywords[this_parent_name],None)
            if _id is None:
                print(f"Warning: The primary key {keywords[this_parent_name]} doesnt exist in ",this_parent_name)
                _id = parent_id
        else:
            #get the id of the dict ( will serve as the parent id for the child dicts if they exist)
            _id = data.get("id",parent_id)
        has_no_id = False
        #if _id is None:
        #    _id = parent_id
            #has_no_id = True
            #print('//',parent_class,parent_relational)
        
        #loop through the elements of the dict
        for key,value in data.items():
            _item_name=item_name+'.'  + key
            _parent_class=parent_class+'.'+ key
            

            #if has_no_id:
            #    parent_class = parent_relational

            _parent_relational=parent_relational+"." + parent_class.split('.')[-1]
            splatter3(value,parent_class=_parent_class,parent_id=_id,item_name=_item_name,
                parent_relational=_parent_relational,parent_relational_id=_id,keywords=keywords)

        #this part creates/populates the df of the data passed in the argument. in other words, the parent 
        
        if parent_class not in dataframes:
            keys = {}
            #create the keys that will be the headers in the dataframe
            for k,v in data.items():
                if type(v) is list:
                    is_list_of_normal_variables = True
                    for e in v:
                        if  type(e) is dict or type(e) is list:
                            is_list_of_normal_variables = False
                            break
                    if is_list_of_normal_variables:
                        keys[k] = [", ".join(v)]
                   
                       

                if not (type(v) is dict) and not (type(v) is list):
                    keys[k] = [v]
                    
            dataframes[parent_class] = pd.DataFrame(data=keys)
        else:
            #add a line to the dataframe with the parent id and the child id
            keys = {}
            #create the keys that will be the headers in the dataframe
            for k,v in data.items():
                if type(v) is list:
                    is_list_of_normal_variables = True
                    for e in v:
                        if  type(e) is dict or type(e) is list:
                            is_list_of_normal_variables = False
                            break
                    if is_list_of_normal_variables:
                        keys[k] = [", ".join(v)]
                   
                       
                if not (type(v) is dict) and not (type(v) is list):
                    keys[k] = [v]
                    
            temp_df = pd.DataFrame(data=keys)
            
            dataframes[parent_class]= dataframes[parent_class].append(temp_df,ignore_index=True)


        #print("////",parent_relational,parent_class,item_name)
        #this part creates the association table, it is only reached if we have a dict where one of its values is also a dict
        if parent_relational != "":
            this_parent_name = parent_class.split('.')[-1]
            this_relational_parent_name = parent_relational.split('.')[-1]
            if this_parent_name in keywords.keys():
                item_id = data.get(keywords[this_parent_name],None)
                if item_id is None:
                    item_id = parent_id
            else:
                #get the id of the dict ( will serve as the parent id for the child dicts if they exist)
                item_id = data.get("id",None)
            #print(parent_relational,parent_relational_id,parent_class,item_id)
            if item_id is not None:
                #print(f"\nbatta ({parent_relational_id}) ({item_id}) [{parent_relational} {parent_class}] {item_name} {data.items()}")
                for k,v in data.items():
                
                    if (parent_relational,f"{parent_class}") not in dataframes:
                        #the keys that will be thea headers in the dataframe
                        parent_relational_key = parent_relational+'.'+ keywords.get(this_relational_parent_name,"id")
                        parent_key = f"{parent_class}." + keywords.get(this_parent_name,"id")
                        #print(this_parent_name,this_relational_parent_name,parent_class,parent_relational,parent_relational_key,parent_key)
                        keys = {
                            strip_dots(parent_relational_key) :[parent_relational_id],
                            strip_dots(parent_key):[item_id]
                        }
                        dataframes[(parent_relational,f"{parent_class}")] = pd.DataFrame(data=keys)
                    else:
                        #add a line to the dataframe with the parent id and the child id
                        dataframes[(parent_relational,f"{parent_class}")].loc[len(dataframes[(parent_relational,f"{parent_class}")].index)] =  [parent_relational_id, item_id]

def find_keys(data):
    keys = []
    if type(data) is dict:
        for k,v in data.items():
            if type(v) is dict or type(v) is list:
                keys.append(k)
            keys += find_keys(v)
    elif type(data) is list:
        for d in data:
            keys += find_keys(d)
    return list(dict.fromkeys(keys))

def product(df1,df2,association_table,df1_name,df2_name,primary_keys):
    keys = {}
    #add the df1 columns to keys
    for key in df1.keys() :
        keys[key] = []
    #add the df2 columns to keys
    #for key in df2.keys() :
    #    keys[df2_name+'.'+key] = []
    keys[df2_name.split(".")[-1]+"."+primary_keys.get(df2_name.split(".")[-1],"id")] = []
    result = pd.DataFrame(data=keys)
    
    """for row in association_table.to_numpy():
        line = df1.loc[df1['id'] == row[0]].values.tolist()[0]+ df2.loc[df2['id'] == row[1]].values.tolist()[0]
        result.loc[len(result)] =  line"""

    for row in df1.to_numpy(): 
        for r in association_table.values.tolist():
            #print("aa",r,'\n',df1.loc[df1['id'] == r[0]])
            if row[0] == r[0]:
                primary_key = primary_keys.get(df2_name.split(".")[-1],"id")
                line = row.tolist()+ df2.loc[df2[primary_key] == r[1]][primary_key].values.tolist()  #.values.tolist()[0]
                result.loc[len(result)] =  line
    
    return result

def create_products(keywords,master="master",primary_keys={}):
    df = dataframes[master]
    for keyword in keywords:
        df = product(df,dataframes[keyword],association_table=dataframes[(master,keyword)],df1_name=master,df2_name=keyword,primary_keys=primary_keys)

    #df = v.drop_duplicates()
    #writer = pd.ExcelWriter("result.xlsx", engine='xlsxwriter')
    #df.index = range(len(df.index))
    #df.to_excel(writer, sheet_name="result")
    #writer.save()
    print("\n\n------------------")
    print("Result master table:\n",df,'\n')
    return df

def read_and_parse_json(primary_keys,keywords,master_table,output_filename=None,filename=None,json_string=None,json_object=None):
    
    if filename:
        with open(filename,'r') as f:
            data = json.load(f)
    elif json_string:
        data = json.loads(json_string)
    elif json_object:
        data = json_object
    else:
        return "Error: the data could not be processed"
    
    data = data if type(data) is list else [data]

        
    for item in data:
        splatter3(data=item,parent_class="",keywords=primary_keys)
        
    # if output_filename:
    #     writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        
    for k,v in dataframes.items():
        if v.empty:
            #print("EMPTY:",k)
            continue
            
        v = v.drop_duplicates()
        dataframes[k] = v
        v.index = range(len(v.index))
        # if output_filename:
        #     v.to_excel(writer, sheet_name=str(k).replace("'","")[:31])
            
        #print output to console
        print("\n\n----------------\n",k,':\n\n',v)

    dfs = [type(v) for v in dataframes.values()]

    # if output_filename:
    #     writer.save()
        
    create_products(master=master_table,keywords=keywords,primary_keys=primary_keys)


# # primary_keys = {"servlet":"server-name", "init-param":"code"}
# # keywords = ["web-app.servlet.init-param"]
# # master_table = "web-app.servlet"
# # filename="servlet.json"


# primary_keys = {"item":"id", "batter":"id", "batter1":"id", "filling":"id", "topping":"id"}
# keywords = ["items.item.topping","items.item.batters.batter"]
# master_table = "items.item"
# filename="example8.json"

# ######################
# ## INSTRUCTIONS:
# ## To load the json from a file, simply specify the filename and pass it to the function
# ## To load json from a string then pass in the the string to the argument json_string
# ## To load json from an object (dict or list) then pass it in the argument json_object
# ## You can do that by replacing filename=filename by json_object=my_object for example
# ## If you dont want to save the files into an excel spreadsheet then dont pass in the argument output_filename
# read_and_parse_json(filename=filename,primary_keys=primary_keys,keywords=keywords,master_table=master_table,output_filename="output.xlsx")
