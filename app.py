import streamlit as st
import pandas as pd
import logic
import itertools

# Set the title of the page
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

room_count = len(selected_rooms)
hall_count = len(selected_halls)

# style
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7ffff')
  ]
                               
td_props = [
  ('font-size', '12px')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

if(st.button("Generate Seating") and file and selected_blocks and (selected_halls or selected_rooms) and branch):
    res = logic.generate(file, selected_blocks, selected_halls, selected_rooms, branch, exam_type)
    print(res)
    for i in res.keys():
        st.write(i)
        outputdframe = (pd.DataFrame(res[i]))
        df2 = outputdframe.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
        st.table(df2)
        st.download_button(label="Download as CSV", data=pd.DataFrame(res[i]).to_csv(), file_name=f"{i}.csv", mime="text/csv")

    #st.write(res)
    

else:
    st.write("Fill all the Fields")
#print(selected_rooms)
#print(selected_halls)



#st.write(f"You selected the {branch} branch.")


    


