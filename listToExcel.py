import xlsxwriter
from xlsxwriter import Workbook
import constants
import matplotlib.pyplot as plt
import numpy as np
from seaborn import heatmap
import seaborn


# filename = filename = constants.ROOTdata +  'twitter' + '\\' +'list2excel' + '.xlsx'
# workbook = xlsxwriter.Workbook(filename)
# worksheet = workbook.add_worksheet('matrix')
#
# list1 = ['oil', 'oil', 'oil', 'oil', 'oil', 'oil', 'oil', 'oil', 'oil', 'oil', 'oil', 'gold', 'gold', 'gold', 'gold', 'gold', 'gold', 'gold', 'gold', 'gold', 'gold', 'gold', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'stockMarket', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'oil_production', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'oil_opec', 'oil_production', 'oil_places', 'oil_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'gold_production', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'gold_production', 'gold_mine', 'gold_places', 'gold_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_market', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_other', 'stockMarket_market', 'stockMarket_places', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_forecast', 'gold_production', 'gold_action1+', 'gold_action2+', 'gold_change3-', 'gold_forecast', 'gold_change2-', 'gold_change3+', 'gold_change1-', 'gold_action2-', 'stockMarket_production', 'stockMarket_action1+', 'stockMarket_action2+', 'stockMarket_change3-', 'stockMarket_forecast', 'stockMarket_change2-', 'stockMarket_change3+', 'stockMarket_change1-', 'stockMarket_action2-', 'gold_production', 'gold_action1+', 'gold_action2+', 'gold_change3-', 'gold_forecast', 'gold_change2-', 'gold_change3+', 'gold_change1-', 'gold_action2-']
# list2 = ['oil_action1+', 'oil_places', 'oil_change2-', 'oil_change1-', 'oil_forecast', 'oil_opec', 'oil_change3+', 'oil_production', 'oil_change3-', 'oil_action2+', 'oil_action2-', 'gold_action1+', 'gold_places', 'gold_change2-', 'gold_mine', 'gold_change1-', 'gold_forecast', 'gold_change3+', 'gold_production', 'gold_change3-', 'gold_action2+', 'gold_action2-', 'stockMarket_action1+', 'stockMarket_places', 'stockMarket_change2-', 'stockMarket_change1-', 'stockMarket_forecast', 'stockMarket_production', 'stockMarket_change3+', 'stockMarket_other', 'stockMarket_change3-', 'stockMarket_action2+', 'stockMarket_action2-', 'stockMarket_market', 'oil_action1+', 'oil_action1+', 'oil_action1+', 'oil_action1+', 'oil_places', 'oil_places', 'oil_places', 'oil_change2-', 'oil_change2-', 'oil_change2-', 'oil_change2-', 'oil_change1-', 'oil_change1-', 'oil_change1-', 'oil_change1-', 'oil_opec', 'oil_opec', 'oil_change3+', 'oil_change3+', 'oil_change3+', 'oil_change3+', 'oil_change3-', 'oil_change3-', 'oil_change3-', 'oil_change3-', 'oil_action2+', 'oil_action2+', 'oil_action2+', 'oil_action2+', 'oil_action2-', 'oil_action2-', 'oil_action2-', 'oil_action2-', 'gold_action1+', 'gold_action1+', 'gold_action1+', 'gold_action1+', 'gold_places', 'gold_places', 'gold_places', 'gold_change2-', 'gold_change2-', 'gold_change2-', 'gold_change2-', 'gold_mine', 'gold_mine', 'gold_change1-', 'gold_change1-', 'gold_change1-', 'gold_change1-', 'gold_change3+', 'gold_change3+', 'gold_change3+', 'gold_change3+', 'gold_change3-', 'gold_change3-', 'gold_change3-', 'gold_change3-', 'gold_action2+', 'gold_action2+', 'gold_action2+', 'gold_action2+', 'gold_action2-', 'gold_action2-', 'gold_action2-', 'gold_action2-', 'stockMarket_action1+', 'stockMarket_action1+', 'stockMarket_action1+', 'stockMarket_action1+', 'stockMarket_action1+', 'stockMarket_places', 'stockMarket_places', 'stockMarket_places', 'stockMarket_places', 'stockMarket_change2-', 'stockMarket_change2-', 'stockMarket_change2-', 'stockMarket_change2-', 'stockMarket_change2-', 'stockMarket_change1-', 'stockMarket_change1-', 'stockMarket_change1-', 'stockMarket_change1-', 'stockMarket_change1-', 'stockMarket_change3+', 'stockMarket_change3+', 'stockMarket_change3+', 'stockMarket_change3+', 'stockMarket_change3+', 'stockMarket_other', 'stockMarket_other', 'stockMarket_other', 'stockMarket_change3-', 'stockMarket_change3-', 'stockMarket_change3-', 'stockMarket_change3-', 'stockMarket_change3-', 'stockMarket_action2+', 'stockMarket_action2+', 'stockMarket_action2+', 'stockMarket_action2+', 'stockMarket_action2+', 'stockMarket_action2-', 'stockMarket_action2-', 'stockMarket_action2-', 'stockMarket_action2-', 'stockMarket_action2-', 'stockMarket_market', 'stockMarket_market', 'oil_production', 'oil_action1+', 'oil_action2+', 'oil_change3-', 'oil_forecast', 'oil_change2-', 'oil_change3+', 'oil_change1-', 'oil_action2-', 'oil_production', 'oil_action1+', 'oil_action2+', 'oil_change3-', 'oil_forecast', 'oil_change2-', 'oil_change3+', 'oil_change1-', 'oil_action2-', 'stockMarket_production', 'stockMarket_action1+', 'stockMarket_action2+', 'stockMarket_change3-', 'stockMarket_forecast', 'stockMarket_change2-', 'stockMarket_change3+', 'stockMarket_change1-', 'stockMarket_action2-']
list3 = [2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 0.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.0, 1.0, 1.0, 2.0, 0.0, 1.0, 0.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.0, 1.0, 1.0, 2.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0]
#
# worksheet.write('A1', 'rows')
# # worksheet.write('B1', 'cols')
# index = 2
# for i in list1:
#     worksheet.write('A'+str(index), i)
#     index = index + 1
#
# workbook.close()

edgeWeights = []
for i in range(0, len(list3)):
    weights = []
    for j in range(0, len(list3)):
        if i != j:
            weights.append(0)
        else:
            weights.append(list3[i])
    edgeWeights.append(weights)

seaborn.heatmap(np.array(edgeWeights))



