



def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result



mydict = {#'coffee':      {  'crop':     'bean crop (conditions OR losses OR harvest OR record)',
                                  # 'weather':  'weather OR frost OR freeze OR storm OR drought',
                                  # 'places':   'brazil OR indonesia OR vietnam OR columbia OR ethiopia'
  #                              },
                  'cocoa':        { 'crop':     'crop (conditions OR losses OR harvest OR record)',
                                  'weather':  'weather OR frost OR freeze OR storm OR drought',
                                  'places':   'ivory coast OR indonesia OR ghana OR liberia'
                                     },
                  'oil':         {   'opec':   'opec (price OR news OR meeting OR eia)',
                                   'places': 'middle east OR syria OR iraq OR israel OR Saudi Arabia OR russia'
                                  },
                'gold':        {  'mine':    'mining (discovery OR strike OR speculation OR newport)',
                                  'places':  'south africa OR russia OR india OR australia'
                                 },
                'stockMarket':  {  'market': 'economy OR bear OR bull OR open (lower OR higher) OR Yellen OR stimulus',
                                  'places': 'China OR Ukraine OR Russia* OR Syria* OR Europe OR \"middle east\"',
                                  'other': '((Bonds OR Notes) (buying OR higher)) OR hedge fund selloff OR oil lower',
                                  },
                # 'hogs':         { 'producers': 'producers OR slaughter OR packers OR feed OR virus',
                #                   'supply': 'pork over supply OR lower sales OR higher exports*',
                #                   'demand': 'pork high demand OR increased sales OR higher imports*',
                #                  },
                # 'palladium':    { 'market': 'automotive OR PAL OR SWC OR Norilsk OR Anglo Platinum OR LDI OR emissions',
                #                   'places': 'mine* (russia OR south africa) OR demand (china OR india or brazil)',
                                  #}
}

print list(find('gold', mydict))