import streamlit as st
import pandas as pd
import pulp as p
from PIL import Image 
def optimize(raw):
    temp=pd.read_excel(raw)
    df=temp.drop(labels=0, axis=0)
    prob = p.LpProblem("myproblem",p.LpMaximize)
    products = list(df.iloc[:,0])
    sp = dict(zip(products,df.iloc[:,1]))
    demand = dict(zip(products,df.iloc[:,2]))
    loopconstraints = []
    for i in range (3,len(df.columns)):
        loopconstraints.append(dict(zip(products,df.iloc[:,i])))
    prod_vars = p.LpVariable.dicts("Item",products,lowBound=0,cat='Continuous')
    df1=temp.iloc[0,:]
    prob += p.lpSum([sp[i]*prod_vars[i] for i in products])
    for i in range (len(loopconstraints)):
        prob += p.lpSum([loopconstraints[i][f] * prod_vars[f] for f in products]) <= df1[i+3]
    for i in range (len(products)):
        prob += prod_vars[products[i]] <= demand[products[i]]       
    prob.solve()
    st.write("Status:", p.LpStatus[prob.status])
    for v in prob.variables():
        if v.varValue>0:
            st.write(v.name, "=", v.varValue)
    obj = p.value(prob.objective)
    st.write("The total cost of this balanced diet is: ${}".format(round(obj,2)))
    return(0)

logo = Image.open("Sun_Pharma_logo.jpg")
st.image(logo,width=50)

st.title("Product Mix Optimiser")
st.write("An webapp to find the right product mix to maximize the revenue")


st.sidebar.write("# Upload excel file in the specified format")
fulltable_1 = st.sidebar.file_uploader(" ", type="xlsx")

if fulltable_1 is None:
	st.warning("You haven't uploaded any file")
else:
  st.write("file uploaded")
  temp10=pd.read_excel(fulltable_1)
  df10=temp10.drop(labels=0, axis=0)


st.sidebar.write(" ")
st.sidebar.info("# Press Optimize to get the right Product Mix")


if fulltable_1 is not None:
  over_view= pd.DataFrame(columns=["No of SKU's",'No of constraints','Total Demand','Potential Revenue'])
  df_dummy = df10.iloc[:,2]*df10.iloc[:,1]
  over_view = over_view.append({"No of SKU's": df10.shape[0], "No of constraints": df10.shape[1]-3, "Total Demand": "{:,.0f}".format(df10.iloc[:,2].sum(axis = 0, skipna = True)), "Potential Revenue": "${:,.0f}".format(df_dummy.sum())}, ignore_index=True)
  st.write(over_view)

if fulltable_1 is not None:
  if st.sidebar.button("Optimize"):
    optimize(fulltable_1)



 