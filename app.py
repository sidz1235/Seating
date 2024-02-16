import streamlit as st
import pandas as pd
import logic
import itertools


def ranges(i):
    i = sorted(set(i))
    for key, group in itertools.groupby(enumerate(i), lambda t: t[1]-t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

# Set the title of the page
st.set_page_config(layout="wide")
st.title("Vasavi College of Engineering")

file = st.file_uploader("Upload a CSV/XLSX/XLS file", type=["csv", "xlsx", "xls"])
exam_type = st.selectbox("Select Examination Type", ["Internal", "External"])
sheet_names = None
branch = None
block_rooms = {"R":["R-201","R-202","R-203","R-301","R-207","R-208","R-308","R-309","R-307","R-302","R-303"],
            "V":["V-209","V-109","V-210","V-312","V-118","V-212","V-110","V-211","V-316","V-117","V-108","V-313","V-119"],
              "J":["J-012","J-112","J-215","J-208","J-106","J-419","J-412","J-007","J-313","J-306","J-301"],
              "C":["C-101","C-107","C-106","C-305","C-301","C-304"],
              "VS":["VS-101","VS-102","VS-201","VS-301","VS-302","VS-303"]}
block_halls = {"R": ["R-204", "R-205", "R-206", "R-304", "R-305", "R-306"]}
branch_codes = {"733":"CSE", "737":"IT", "735":"ECE", "734":"EEE", "748":"AIML", "732":"CIVIL", "736":"MECH"}


selected_rooms = []
selected_halls = []
selected_blocks = []
capacities = []

if file is not None:
    with pd.ExcelFile(file) as xls:
        sheet_names = xls.sheet_names
        selected_sheet = st.selectbox("Select Sheet", sheet_names)
        df = pd.read_excel(xls, sheet_name=selected_sheet)
    
    st.write(df)
    #st.download_button(label="Download as CSV", data=df.to_csv(), file_name="data.csv", mime="text/csv")

# Create a dropdown menu to select the branch
if(sheet_names is not None):
    branch = st.multiselect("Select Branch", sheet_names)
#num_rooms = st.number_input("Enter Number of Rooms", step=1, value=0, min_value = 0)
#num_halls = st.number_input("Enter Number of Halls", step=1, value=0, min_value = 0)
selected_blocks = st.multiselect("Select Blocks", list(block_rooms.keys()))

for block in selected_blocks:
    rooms = st.multiselect("Select Rooms in Block " + str(block), block_rooms[block])
    selected_rooms.extend(rooms)

for block in selected_blocks:
    if(block in block_halls.keys()):
        halls = st.multiselect("Select Halls in Block " + str(block), block_halls[block])
        selected_halls.extend(halls)

#selected_rooms = set(selected_rooms)
#selected_halls = set(selected_halls)

room_count = len(selected_rooms)
hall_count = len(selected_halls)

# style
# th_props = [
#   ('font-size', '10px'),
#   ('text-align', 'center'),
#   ('font-weight', 'bold'),
#   ('color', '#6d6d6d'),
#   ('background-color', '#f7ffff')
#   ]
                               
# td_props = [
#   ('font-size', '10px')
#   ]
                                 
# styles = [
#   dict(selector="th", props=th_props),
#   dict(selector="td", props=td_props)
#   ]

capacities = st.selectbox("Select Capacity", [30, 45, 60])

if(st.button("Generate Seating") and file and selected_blocks and (selected_halls or selected_rooms) and branch):
    res = logic.generate(file, selected_blocks, selected_halls, selected_rooms, branch, exam_type, capacities)
    #print(res)
    cur_row = 0
    cur_col = 0

    tab_list = st.tabs(list(res.keys()))
    tab_number = 0

    for i in res.keys():
        with tab_list[tab_number]:
            st.write(i)

            dist_branches = []
            for x in range(len(res[i])):
                for y in range(len(res[i][x])):
                    #print(((str(room[x][y][0])).split("-"))[2])
                    try:
                        if(((str(res[i][x][y][0])).split("-")) not in dist_branches):
                            dist_branches.append(((str(res[i][x][y][0])).split("-"))[2])
                        
                        if(((str(res[i][x][y][1])).split("-")) not in dist_branches):
                            dist_branches.append(((str(res[i][x][y][1])).split("-"))[2])
                    except:
                        pass
            
            dist_branches = list(set(dist_branches))
            dist_branches = [[0, dist_branches[k], [], []] for k in range(len(dist_branches))]

            count = 0

            for x in range(len(res[i])):
                for y in range(len(res[i][x])):
                    try:
                        if(res[i][x][y][0] != -1):
                            count += 1
                        if(res[i][x][y][1] != -1):
                            count += 1
                    except:
                        pass
            
            #st.write("Branch".center(10)+"Number of Students".center(30))

            for x in range(len(res[i])):
                cur_col = 0
                for y in range(len(res[i][x])):
                    cur_col += 1
                    try:
                        quote = str(res[i][x][y][0]).center(20)
                        for z in range(len(dist_branches)):
                            if(dist_branches[z][1] == ((str(res[i][x][y][0])).split("-"))[2]):
                                dist_branches[z][0] += 1
                                dist_branches[z][2].append(int(((str(res[i][x][y][0])).split("-"))[3]))
                                dist_branches[z][3].append(int("".join(((str(res[i][x][y][0])).split("-")))))
                    except:
                        pass

                    try:
                        quote += str(res[i][x][y][1]).center(20)
                        for z in range(len(dist_branches)):
                            if(dist_branches[z][1] == ((str(res[i][x][y][1])).split("-"))[2]):
                                dist_branches[z][0] += 1
                                dist_branches[z][2].append(int(((str(res[i][x][y][1])).split("-"))[3]))
                                dist_branches[z][3].append(int("".join(((str(res[i][x][y][1])).split("-")))))
                        
                    except:
                        pass

            for x in range(len(res[i])):
                for y in range(len(res[i][x])):
                    for z in range(len(res[i][x][y])):
                        if(len(res[i][x][y][z]) > 2):
                            res[i][x][y][z] = res[i][x][y][z][5:]
                            
            outputdframe = (pd.DataFrame(res[i]))
            
            output_df = pd.DataFrame(res[i]).rename(columns={0: 'Desk-1', 1: 'Desk-2', 2: 'Desk-3', 3: 'Desk-4', 4: 'Desk-5', 5: 'Desk-6'})  
            #df2 = output_df.style.set_properties(**{'text-align': 'center'})

            st.dataframe(output_df, hide_index = True, use_container_width = True)


            total = 0
            for k in range(len(dist_branches)):
                #print(dist_branches[i][2])
                dist_branches[k][2].sort()
                dist_branches[k][3].sort()
                
                #print(list(ranges(dist_branches[i][3])))
                
                #print(dist_branches[i][2])
                temp_string = ""
                temp_string += (str(branch_codes[dist_branches[k][1]]).center(60))
                print(dist_branches[k])
                for j in range(len(list(ranges(dist_branches[k][3])))):
                    tem = list(ranges(dist_branches[k][3]))
                    print(tem[j][0], tem[j][1])
                    if(tem[j][0] == tem[j][1]):
                        temp_string += (str(str(tem[j][0])[:4]+"-"+str(tem[j][0])[4:6]+"-"+str(tem[j][0])[6:9]+"-"+str(tem[j][0])[9:]+",  ").center(30))
                    else:
                        temp_string += (str(str(tem[j][0])[:4]+"-"+str(tem[j][0])[4:6]+"-"+str(tem[j][0])[6:9]+"-"+str(tem[j][0])[9:]+" To "+str(tem[j][1])[:4]+"-"+str(tem[j][1])[4:6]+"-"+str(tem[j][1])[6:9]+"-"+str(tem[j][1])[9:]+",  ").center(30))
                total += dist_branches[k][0]
                temp_string += str(dist_branches[k][0]).center(60)
                st.write(temp_string)

            st.write("Total: " + str(total).center(60))
            st.divider()
            tab_number += 1

    #st.write(res)
    

else:
    st.write("Fill all the Fields")
#print(selected_rooms)
#print(selected_halls)



#st.write(f"You selected the {branch} branch.")


    


