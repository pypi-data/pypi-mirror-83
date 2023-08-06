def bayes_suspects_cum(df,event,suspects,point,interval='NULL',min='NULL'):
    """Importing what we need"""
    
    import itertools
    from itertools import combinations 
    import scipy
    from sklearn.preprocessing import StandardScaler
    import scipy.stats
    from statsmodels.distributions.empirical_distribution import ECDF
    import pandas as pd
    import numpy as np
    
    """Checking the presence of optimal parameters"""
    if interval == 'NULL':
        interval = 0.05
    else:
        interval = interval

    if min == 'NULL':
        min = 10
    else:
        min = min
    
    """Defining useful functions"""
    def odd_even(num):
        if (num % 2) == 0:
           return 'Even'
        else:
           return 'Odd'
    
    def mult_formula_cum(elements,df,point):

        """elements: list of elements, list format"""
        """df: dataframe"""
        """point: dictionary"""
        df_final = pd.DataFrame()
    
        for i in range(len(elements)):

            a = 1
            olist = list(elements[i])
            #print(olist)


            while len(olist)>0:
                nlist = olist.copy()
                #print(nlist[0])
                del nlist[0]
                #print(nlist)

                dff = df.copy()

                for e in nlist:
                    dff1 = dff[dff[e]<=point[e]]
                    dff = dff1.copy()

                """Calculating the ECDF and probabilities"""
                prob = ECDF(dff[olist[0]])(point[olist[0]])
                a = prob*a
                #print(a)

                """Adjusting the list"""
                olist = nlist.copy()
                #print(olist)

            final2 = pd.DataFrame(
                {
                'name': str(elements[i]),
                'number_of_variables': len(elements[i]),
                'prob_ba':a,
                'number_type':odd_even(len(elements[i]))
                }, index=[0])

            df_final = pd.concat([df_final,final2])

        return df_final


    """Getting all possible combinations"""
    all_combinations = []
    for r in range(1,len(suspects) + 1):

        combinations_object = itertools.combinations(suspects, r)
        combinations_list = list(combinations_object)
        all_combinations += combinations_list

    cond1 = mult_formula_cum(elements = list(all_combinations) ,df = df[df[event]<=point[event]],point = point)
    cond2 = mult_formula_cum(elements = list(all_combinations) ,df = df,point = point)

    prob_a = ECDF(df[event])(point[event])
   
    
    cond = pd.merge(cond1,cond2,how='inner',on= ['name','number_of_variables','number_type'])
    cond['bayes']= cond['prob_ba_x']/cond['prob_ba_y']*prob_a
    
    cond['bayes_total'] = (cond['prob_ba_x']/cond['prob_ba_y']*prob_a)*cond['prob_ba_y']
    
    del cond['prob_ba_x']
    del cond['prob_ba_y']
    
    
    individual = cond[(cond['number_of_variables']==1)].bayes_total.sum()
    intersection_odd = cond[(cond['number_type']=='Odd')&
    (cond['number_of_variables']>1)].bayes_total.sum()
    intersection_even = cond[(cond['number_type']=='Even')&
    (cond['number_of_variables']>1)].bayes_total.sum()

    space = individual - intersection_odd + intersection_even
    total = cond['bayes_total'].sum()
    
    cond['bayes_total_final'] = space*cond['bayes_total']/total
    cond['bayes_total'] = cond['bayes_total_final']
    
    del cond['bayes_total_final']
    
    return cond