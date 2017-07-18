MIT License

Copyright (c) 2017 Jonathan Pelham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

def classifier_intersection(database,list_of_classifiers,venn_required=False,plot_names=False,save_path=False,normalize=False, output_table_path=False,title_needed=False,plot_labels=True):
    from matplotlib import pyplot as plt
    from matplotlib_venn import venn3,venn2, venn2_circles, venn3_circles
    from tabulate import tabulate

    if isinstance(list_of_classifiers, str):
        no_of_classifiers =1
        list_of_classifiers=[list_of_classifiers,'padding']
    elif isinstance(list_of_classifiers, str):
        no_of_classifiers =1
        list_of_classifiers=[list_of_classifiers,'padding']            
    else:
        no_of_classifiers = len(list_of_classifiers) 
        list_of_classifiers=list_of_classifiers
    
    if not 2 <= no_of_classifiers <= 3:
        print("Wrong number of classifiers in set.  Venn plotting method can only handle 2 or 3")
    
    if no_of_classifiers==2:
        """For sets A & B
            A only
            B only
            A & B
            """
        total_in_set=len(database)
        zeroth= database.groupby(list_of_classifiers[0]).size()
        print("'%s' has %d True & %d False.  Total valid rows %d" % (list_of_classifiers[0],zeroth[True],zeroth[False],zeroth[True]+zeroth[False]))
        first= database.groupby(list_of_classifiers[1]).size()
        print("'%s' has %d True & %d False.  Total valid rows %d" % (list_of_classifiers[1],first[True],first[False],first[True]+first[False]))         
        Aonly=database[(database[list_of_classifiers[0]]==True) & (database[list_of_classifiers[1]]==False)]
        Bonly=database[(database[list_of_classifiers[0]]==False) & (database[list_of_classifiers[1]]==True)]
        AandB=database[(database[list_of_classifiers[0]]==True) & (database[list_of_classifiers[1]]==True)] 
        negative_class_rows=database[(database[list_of_classifiers[0]]==False) & (database[list_of_classifiers[1]]==False)] 
        Acount=len(Aonly)
        Bcount=len(Bonly)
        AandBcount=len(AandB) 
        negative_class=len(negative_class_rows)
        positive_class=Acount+Bcount+AandBcount
        missing_row_check=positive_class+negative_class
        print("Positive Class %d plus Negative class %d is %d" % (positive_class,negative_class,missing_row_check))
        if (total_in_set-missing_row_check)>0:
            print("The number of missing rows is %d" % (total_in_set-missing_row_check,))
        print("The total no of elements is %d of which %d are '%s' only, %d are '%s' only, %d are shared between '%s' & '%s', & %d are classified negative by all. \nThere are %d of '%s' in total & %d of '%s'" % (
        total_in_set,
        Acount,
        list_of_classifiers[0],
        Bcount,
        list_of_classifiers[1],
        AandBcount,
        list_of_classifiers[0],
        list_of_classifiers[1],
        negative_class,
        Acount+AandBcount,
        list_of_classifiers[0],
        Bcount+AandBcount,
        list_of_classifiers[1]))
        if output_table_path:
            Acount_label='%s only' % (plot_names[1],)
            Bcount_label='%s only'  % (plot_names[2],)
            AandBcount_label='%s & %s'  % (plot_names[1],plot_names[2])
            table=[
                [Acount_label, Acount,(float(Acount)/float(total_in_set))*100,Acount],
                [Bcount_label,Bcount,(float(Bcount)/float(total_in_set))*100,Acount+Bcount],
                [AandBcount_label,AandBcount,(float(AandBcount)/float(total_in_set))*100,Acount+Bcount+AandBcount]
                ]
            headers=['Subset','Qty','% of Set','Running Total']
            f = open(output_table_path, 'w')
            f.write(tabulate(table, headers, tablefmt="latex"))
            a_explanation='\\multicolumn{4}{|c|}{%s total set %f%% %d = %d + %d }\\\\' % (plot_names[1],((AandBcount+Acount)/float(total_in_set))*100,(AandBcount+Acount),Acount,AandBcount)
            b_explanation='\\multicolumn{4}{|c|}{%s total set %f%% %d = %d + %d }\\\\' % (plot_names[2],((AandBcount+Bcount)/float(total_in_set))*100,(AandBcount+Bcount),Bcount,AandBcount)
            everything_explanation='\\multicolumn{4}{|c|}{Total possible NFF in set %f%% %d = %d + %d + %d }\\\\' % (((AandBcount+Bcount+Acount)/float(total_in_set))*100,(AandBcount+Bcount+Acount),Acount,Bcount,AandBcount)
            to_file='\n'+a_explanation+'\n'+b_explanation+'\n'+everything_explanation
            f.write(to_file)
            f.close()
            print(tabulate(table, headers))
        if normalize:
            classifier_intersection_tuple=(Acount/total_in_set,Bcount/total_in_set,AandBcount/total_in_set) 
        else:
            classifier_intersection_tuple=(Acount,Bcount,AandBcount)   
        if venn_required:
            plt.figure(figsize=(4,4))   
            a_set=Acount+AandBcount
            b_set=Bcount+AandBcount
            a_data_string="\nQty %d or %d%% of MWO" % (a_set,(float(a_set)/float(total_in_set))*100)
            b_data_string="\nQty %d or %d%% of MWO" % (b_set,(float(b_set)/float(total_in_set))*100)
            a_string=plot_names[1]+a_data_string
            b_string=plot_names[2]+b_data_string
            if plot_labels:
                v=venn2(subsets=classifier_intersection_tuple, set_labels = (a_string, b_string))
            else:
                v=venn2(subsets=classifier_intersection_tuple,set_labels = ('', ''))
            c = venn2_circles(subsets=classifier_intersection_tuple, linestyle='solid')  
            c[0].set_lw(1.0)
            c[1].set_lw(1.0)
            if title_needed:
                data_string=" %d MWO\nTotal MWO NFF %d or %d%%" % (total_in_set,positive_class,(float(positive_class)/float(total_in_set))*100)
                title_string=plot_names[0]+data_string
                print(title_string)
                plt.title(title_string,y=-0.25)       
            if save_path:
                if isinstance(save_path,str):
                    plt.savefig(save_path, bbox_inches='tight',dpi=900)
                else:
                    raise TypeError('save_path is not a string')
            plt.show()
    elif no_of_classifiers==3:
        """For sets A, B, & C
            A only
            B only
            A & B but not C
            C only
            A & C but not B
            B & C but not A
            A & B & C
            """
        total_in_set=len(database)
        zeroth= database.groupby(list_of_classifiers[0]).size()
        print("'%s' has %d True & %d False.  Total valid rows %d" % (list_of_classifiers[0],zeroth[True],zeroth[False],zeroth[True]+zeroth[False]))
        first= database.groupby(list_of_classifiers[1]).size()
        print("'%s' has %d True & %d False.  Total valid rows %d" % (list_of_classifiers[1],first[True],first[False],first[True]+first[False]))     
        second= database.groupby(list_of_classifiers[2]).size()  
        print("'%s' has %d True & %d False.  Total valid rows %d" % (list_of_classifiers[2],second[True],second[False],second[True]+second[False]))   
        Aonly=database[(database[list_of_classifiers[0]]==True) & (database[list_of_classifiers[1]]==False) & (database[list_of_classifiers[2]]==False)]
        Bonly=database[(database[list_of_classifiers[0]]==False) & (database[list_of_classifiers[1]]==True) & (database[list_of_classifiers[2]]==False)]
        AandBnotC=database[(database[list_of_classifiers[0]]==True) & (database[list_of_classifiers[1]]==True) & (database[list_of_classifiers[2]]==False)] 
        Conly=database[(database[list_of_classifiers[0]]==False) & (database[list_of_classifiers[1]]==False) & (database[list_of_classifiers[2]]==True)]
        AandCnotB=database[(database[list_of_classifiers[0]]==True) & (database[list_of_classifiers[1]]==False) & (database[list_of_classifiers[2]]==True)]
        BandCnotA=database[(database[list_of_classifiers[0]]==False) & (database[list_of_classifiers[1]]==True) & (database[list_of_classifiers[2]]==True)]
        AandBandC=database[(database[list_of_classifiers[0]]==True) & (database[list_of_classifiers[1]]==True) & (database[list_of_classifiers[2]]==True)]
        negative_class_rows=database[(database[list_of_classifiers[0]]==False) & (database[list_of_classifiers[1]]==False) & (database[list_of_classifiers[2]]==False)]
        Acount=len(Aonly)
        Bcount=len(Bonly)
        AandBnotCcount=len(AandBnotC)
        Ccount=len(Conly)
        AandCnotBcount=len(AandCnotB)
        BandCnotAcount=len(BandCnotA)
        AandBandCcount=len(AandBandC)
        positive_class=Acount+Bcount+AandBnotCcount+Ccount+AandCnotBcount+BandCnotAcount+AandBandCcount
        negative_class=len(negative_class_rows)
        missing_row_check=positive_class+negative_class
        print("Positive Class %d plus Negative class %d is %d" % (positive_class,negative_class,missing_row_check))
        if (total_in_set-missing_row_check)>0:
            print("The number of missing rows is %d" % (total_in_set-missing_row_check,))
        print("The total no of elements is %d of which %d are '%s' only, %d are '%s' only, & %d are '%s' only. \nThere are %d of '%s' in total, %d of '%s', & %d of '%s'" % (
        total_in_set,
        Acount,
        list_of_classifiers[0],
        Bcount,
        list_of_classifiers[1],
        Ccount,
        list_of_classifiers[2],
        Acount+AandBnotCcount+AandCnotBcount+AandBandCcount,
        list_of_classifiers[0],
        Bcount+AandBnotCcount+BandCnotAcount+AandBandCcount,
        list_of_classifiers[1],
        Ccount+BandCnotAcount+AandCnotBcount+AandBandCcount,
        list_of_classifiers[2]))
        if output_table_path:
            Acount_label='%s only' % (plot_names[1],)
            Bcount_label='%s only'  % (plot_names[2],)
            Ccount_label='%s only'  % (plot_names[3],)
            AandBnotCcount_label='%s & %s only.  No %s'  % (plot_names[1],plot_names[2],plot_names[3])
            AandCnotBcount_label='%s & %s only.  No %s' % (plot_names[1],plot_names[3],plot_names[2])
            BandCnotAcount_label='%s & %s only.  No %s' % (plot_names[2],plot_names[3],plot_names[1])
            AandBandCcount_label='%s, %s & %s' % (plot_names[1],plot_names[2],plot_names[3])
            table=[
                [Acount_label, Acount,(float(Acount)/float(total_in_set))*100,Acount],
                [Bcount_label,Bcount,(float(Bcount)/float(total_in_set))*100,Acount+Bcount],
                [Ccount_label,Ccount,(float(Ccount)/float(total_in_set))*100,Acount+Bcount+Ccount],
                [AandBnotCcount_label,AandBnotCcount,(float(AandBnotCcount)/float(total_in_set))*100,Acount+Bcount+Ccount+AandBnotCcount],
                [AandCnotBcount_label,AandCnotBcount,(float(AandCnotBcount)/float(total_in_set))*100,Acount+Bcount+Ccount+AandBnotCcount+AandCnotBcount],
                [BandCnotAcount_label,BandCnotAcount,(float(BandCnotAcount)/float(total_in_set))*100,Acount+Bcount+Ccount+AandBnotCcount+AandCnotBcount+BandCnotAcount],
                [AandBandCcount_label,AandBandCcount,(float(AandBandCcount)/float(total_in_set))*100,Acount+Bcount+Ccount+AandBnotCcount+AandCnotBcount+BandCnotAcount+AandBandCcount]
                ]
            headers=['Subset','Qty','% of Set','Running Total']
            f = open(output_table_path, 'w')
            f.write(tabulate(table, headers, tablefmt="latex"))
            a_explanation='\\multicolumn{4}{|c|}{%s total set %f%% %d = %d + %d + %d + %d \\\\' % (plot_names[1],((Acount+AandBnotCcount+AandCnotBcount+AandBandCcount)/float(total_in_set))*100,(Acount+AandBnotCcount+AandCnotBcount+AandBandCcount),Acount,AandBnotCcount,AandCnotBcount,AandBandCcount)
            b_explanation='\\multicolumn{4}{|c|}{%s total set %f%% %d = %d + %d + %d + %d \\\\' % (plot_names[2],((Bcount+AandBnotCcount+BandCnotAcount+AandBandCcount)/float(total_in_set))*100,(Bcount+AandBnotCcount+BandCnotAcount+AandBandCcount),Bcount,AandBnotCcount,BandCnotAcount,AandBandCcount)
            c_explanation='\\multicolumn{4}{|c|}{%s total set %f%% %d = %d + %d + %d + %d \\\\' % (plot_names[3],((Ccount+AandCnotBcount+BandCnotAcount+AandBandCcount)/float(total_in_set))*100,(Ccount+AandCnotBcount+BandCnotAcount+AandBandCcount),Ccount,AandCnotBcount,BandCnotAcount,AandBandCcount)
            everything_explanation='\\multicolumn{4}{|c|}{Total possible NFF in set %f%% %d = %d + %d + %d + %d + %d + %d + %d \\\\' % (((Acount+Bcount+Ccount+AandBnotCcount+AandCnotBcount+BandCnotAcount+AandBandCcount)/float(total_in_set))*100,(Acount+Bcount+Ccount+AandBnotCcount+AandCnotBcount+BandCnotAcount+AandBandCcount),Acount,Bcount,Ccount,AandCnotBcount,BandCnotAcount,AandBnotCcount,AandBandCcount)
            to_file='\n'+a_explanation+'\n'+b_explanation+'\n'+c_explanation+'\n'+everything_explanation
            f.write(to_file)
            f.close()
            print(tabulate(table, headers))
        if normalize:
            total_in_set=float(total_in_set)
            norm_Acount=round(float(Acount/total_in_set)*100,2)
            norm_Bcount=round(float(Bcount/total_in_set)*100,2)
            norm_AandBnotCcount=round(float(AandBnotCcount/total_in_set)*100,2)
            norm_Ccount=round(float(Ccount/total_in_set)*100,2)
            norm_AandCnotBcount=round(float(AandCnotBcount/total_in_set)*100,2)
            norm_BandCnotAcount=round(float(BandCnotAcount/total_in_set)*100,2)
            norm_AandBandCcount=round(float(AandBandCcount/total_in_set)*100,2)
            classifier_intersection_tuple=(norm_Acount,norm_Bcount,norm_AandBnotCcount,norm_Ccount,norm_AandCnotBcount,norm_BandCnotAcount,norm_AandBandCcount)
        else:        
            classifier_intersection_tuple=(Acount,Bcount,AandBnotCcount,Ccount,AandCnotBcount,BandCnotAcount,AandBandCcount)  
        if venn_required:  
            plt.figure(figsize=(4,4))
            a_set=Acount+AandBnotCcount+AandCnotBcount+AandBandCcount
            b_set=Bcount+AandBnotCcount+BandCnotAcount+AandBandCcount
            c_set=Ccount+AandCnotBcount+BandCnotAcount+AandBandCcount
            a_data_string="\nQty %d or %d%% of MWO" % (a_set,(float(a_set)/float(total_in_set))*100)
            b_data_string="\nQty %d or %d%% of MWO" % (b_set,(float(b_set)/float(total_in_set))*100)
            c_data_string="\nQty %d or %d%% of MWO" % (c_set,(float(c_set)/float(total_in_set))*100)
            a_string=plot_names[1]+a_data_string
            b_string=plot_names[2]+b_data_string
            c_string=plot_names[3]+c_data_string
            if plot_labels:
                v=venn3(subsets=classifier_intersection_tuple, set_labels = (a_string, b_string,c_string))  
            else:
                v=venn3(subsets=classifier_intersection_tuple,set_labels = ('', '', ''))
            c = venn3_circles(subsets=classifier_intersection_tuple, linestyle='solid')  
            c[0].set_lw(1.0)
            c[1].set_lw(1.0)
            c[2].set_lw(1.0)
            if title_needed:
                data_string=" %d MWO\nTotal MWO NFF %d or %d%%" % (total_in_set,positive_class,(float(positive_class)/float(total_in_set))*100)
                title_string=plot_names[0]+data_string
                print(title_string)
                plt.title(title_string,y=-0.25)             
            if save_path:
                if isinstance(save_path,str):
                    plt.savefig(save_path, bbox_inches='tight',dpi=900)
                else:
                    raise TypeError('save_path is not a string')
            plt.show()
    
    return classifier_intersection_tuple,negative_class_rows
