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
# st.set_page_config(layout="wide")
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

if(sheet_names is not None):
    branch = st.multiselect("Select Branch", sheet_names)

selected_blocks = st.multiselect("Select Blocks", list(block_rooms.keys()))

for block in selected_blocks:
    rooms = st.multiselect("Select Rooms in Block " + str(block), block_rooms[block])
    selected_rooms.extend(rooms)

for block in selected_blocks:
    if(block in block_halls.keys()):
        halls = st.multiselect("Select Halls in Block " + str(block), block_halls[block])
        selected_halls.extend(halls)

room_count = len(selected_rooms)
hall_count = len(selected_halls)

if(exam_type == "Internal"):
    capacities = st.selectbox("Select Capacity", [30, 45, 60])
else:
    capacities = 0

if(st.button("Generate Seating") and file and selected_blocks and (selected_halls or selected_rooms) and branch):
    res = logic.generate(file, selected_blocks, selected_halls, selected_rooms, branch, exam_type, capacities)
    #print(res)
    cur_row = 0
    cur_col = 0

    for i in res.keys():
            st.header('Vasavi College Of Engineering')
            st.markdown("<br>",unsafe_allow_html=True)
            
            st.subheader("Room No : " + i)
           
            dist_branches = []
            for x in range(len(res[i])):
                for y in range(len(res[i][x])):
                    
                    try:
                        if(((str(res[i][x][y][0])).split("-")) not in dist_branches):
                            dist_branches.append(((str(res[i][x][y][0])).split("-"))[2])
                    except:
                        pass

                    try:
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
            

            if(i in selected_halls):
                st.dataframe(output_df, hide_index = True, use_container_width = True, height = 422)
            else:
                st.dataframe(output_df, hide_index = True, use_container_width = True)


            total = 0
            branch_mem = {}
            for k in range(len(dist_branches)):
               
                dist_branches[k][2].sort()
                dist_branches[k][3].sort()

                branch_name = (str(branch_codes[dist_branches[k][1]]).center(60))
                
                branch_list = ""
                for j in range(len(list(ranges(dist_branches[k][3])))):
                    tem = list(ranges(dist_branches[k][3]))
                    print(tem[j][0], tem[j][1])
                    if(tem[j][0] == tem[j][1]):
                        branch_list += (str(str(tem[j][0])[:4]+"-"+str(tem[j][0])[4:6]+"-"+str(tem[j][0])[6:9]+"-"+str(tem[j][0])[9:]+",  ").center(30))
                    else:
                        branch_list += (str(str(tem[j][0])[:4]+"-"+str(tem[j][0])[4:6]+"-"+str(tem[j][0])[6:9]+"-"+str(tem[j][0])[9:]+" To "+str(tem[j][1])[:4]+"-"+str(tem[j][1])[4:6]+"-"+str(tem[j][1])[6:9]+"-"+str(tem[j][1])[9:]+",  ").center(30))
                total += dist_branches[k][0]
                branch_strength = str(dist_branches[k][0]).center(60)
                
                branch_mem[str(k)] = [branch_name,branch_list,branch_strength]

            branch_df = pd.DataFrame(branch_mem).T

            branch_df = branch_df.rename(columns = {0:"Branch",1:"Hall Ticket No",2:"Branch Total"})

            st.dataframe(branch_df,hide_index = True)

            st.write(f"Total Number of Students in Room No {i}    :  " + str(total).center(60))

            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.divider()



else:
    st.write("Fill all the Fields")



    


