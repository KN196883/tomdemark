def get_tdsequential(data, toShow=0):
    if toShow == 0:
        toShow = len(data)
    logging.info('TDシーケンシャル計算中...')

    o=[data.iloc[j]['Open'] for j in range(0, len(data))]
    h=[data.iloc[j]['High'] for j in range(0, len(data))]
    l=[data.iloc[j]['Low'] for j in range(0, len(data))]
    c=[data.iloc[j]['Close'] for j in range(0, len(data))]
    t=[datetime.strptime(data.iloc[j]['Date'], datefmt) for j in range(0, len(data))]

    shortVal=[]
    longVal =[]
    shortCount = 0
    longCount = 0
    for k in range(0,len(c)): #generate TD buy/sell setups
        if k <= 3:
            longCount = 0
            shortCount = 0
    #     if shortCount > 8:
    #         shortCount = 0
    #     if longCount > 8:
    #         longCount = 0
        ## 上、別に9日以上続いてもセットアップカウント続けてもいいんじゃないの？
        if k > 3:
            if c[k] < c[k-4]:
                longCount+=1
            else:
                longCount = 0
            if c[k] > c[k-4]:
                shortCount+=1
            else:
                shortCount = 0
        longVal.append(longCount)
        shortVal.append(shortCount)

    buyVal =[]
    sellVal=[]
    buyCount=0
    sellCount=0
    for y in range(0,len(c)): #generate TD buy countdown
        if y < 11:
            buyCount = 0
        if y>= 11:
            if buyCount == 0:
#                 if h[y] >= l[y-3] or h[y] >= l[y-4] or h[y] >= l[y-5] or h[y] >= l[y-6] or h[y] >= l[y-7]:
#                 if 8 in longVal[y-16:y] or 9 in longVal[y-15:y]:
#                     if c[y] < l[y-2]:
                if 8 in longVal[y-16:y] and h[y] > max(l[y-3], l[y-4], l[y-5], l[y-6], l[y-7]):
                    # セットアップの8日目以降であって、
                    # その日の高値が3日以上前の安値より高いとき、カウントダウンは始められる
                    # ★これはインターセクションが始まっていることの定義
                    if c[y] < l[y - 2]:
                        # その日の終値が、2日前の安値より安いとき、カウントする
                        buyCount += 1
            if buyVal[-1] == 13 or shortVal[y] > 8:
                # カウントダウン13になった or 売りセットアップが整ったなら、カウント終了
                buyCount = 0
            if buyCount != 0:
                # カウントが始まっているということは、インターセクションが始まってることが既に確認されている
                # なので、単純に2日前の安値と今日の終値を比較するだけでよい
                if c[y] < l[y-2]:
                    buyCount += 1
                if longVal[y] == 9:
                    buyCount = 0
        buyVal.append(buyCount)

    for y in range(0,len(c)): #generate TD sell countdown
        if y < 11:
            sellCount = 0
        if y>= 11:
            if sellCount == 0:
                if l[y] <= h[y-3] or l[y] <= h[y-4] or l[y] <= h[y-5] or l[y] <= h[y-6] or l[y] <= h[y-7]:
                    if 8 in shortVal[y-16:y] or 9 in shortVal[y-15:y]:
                        if c[y] > h[y-2]:
                            sellCount = 1
            if sellVal[-1] == 13 or longVal[y] > 8:
                sellCount = 0
            if sellCount != 0:
                if c[y] > h[y-2]:
                    sellCount += 1
                if shortVal[y] == 9:
                    sellCount = 0
        sellVal.append(sellCount)

    d = len(c) - toShow
    if d > 1:
            del o[:d]
            del h[:d]
            del l[:d]
            del c[:d]
            del t[:d]
            del longVal[:d]
            del shortVal[:d]
            del buyVal[:d]
            del sellVal[:d]

    logging.info('計算終了')
    return t, o, h, l, c, shortVal, longVal, sellVal, buyVal


def plot_tdseq(t, o, h, l, c, shortVal, longVal, sellVal, buyVal, savefigname=None):
    logging.info('プロット中...')

    padding = (max(h) - min(l)) * 0.08

    fig, ax = plt.subplots(1,1, figsize=(15,7), dpi=300)
    fig.set_facecolor('white')
    ax.set_facecolor('k')

    # お色
    td_ctdwn_sell_col = 'lime'
    td_ctdwn_buy_col = 'red'
    td_ctdwn_complete_sell_col = "lime"
    td_ctdwn_complete_buy_col = "red"
    td_setup_short_col = 'greenyellow'
    td_setup_long_col = 'lightsalmon'
    td_setup_complete_short_col = "greenyellow"
    td_setup_complete_long_col = "lightsalmon"

    logging.info('値動きプロット中...')
    for z in range(0,len(c)):
        plt.vlines(t[z], ymin=l[z], ymax=h[z], color="white")
        plt.hlines(o[z], xmin=t[z]-timedelta(hours=12), xmax=t[z], color="white")
        plt.hlines(c[z], xmin=t[z], xmax=t[z]+timedelta(hours=12), color="white")

    logging.info('TDシーケンシャルプロット中...')
    #display td countdown values
    for z in range(0,len(c)):
        if int(sellVal[z]) > 10 and int(sellVal[z]) != int(sellVal[z-1]):
            ax.annotate(str(sellVal[z]), xy = (t[z], h[z]+padding),
                        xytext = (t[z], h[z]+padding), size=11,
                        color=td_ctdwn_sell_col, weight='bold',
                        horizontalalignment='center')
        if int(buyVal[z]) > 10 and int(buyVal[z]) != int(buyVal[z-1]):
            ax.annotate(str(buyVal[z]), xy = (t[z], l[z]-padding),
                        xytext = (t[z], l[z]-padding), size=11,
                        color=td_ctdwn_buy_col, weight='bold',
                        horizontalalignment='center')
        #insert arrows when countdown completes
        if sellVal[z] == 13:
            plt.annotate('▼', xy=(t[z], h[z] + 2 * padding), xytext=(t[z], h[z] + 2 * padding),
                         color=td_ctdwn_complete_sell_col, horizontalalignment='center', verticalalignment='center', size=13)
        if buyVal[z] == 13:
            plt.annotate('▲', xy=(t[z], h[z] - 2 * padding), xytext=(t[z], h[z] - 2 * padding),
                         color=td_ctdwn_complete_buy_col, horizontalalignment='center', verticalalignment='center', size=13)

    #display td setup values
    for r in range(0,len(c)):
        if int(shortVal[r]) > 0:
            ax.annotate(str(shortVal[r]), 
                        xy = (t[r], h[r] + padding),
                        xytext = (t[r], h[r] + padding),
                        color=td_setup_short_col,
                        size=10,weight='bold',
                        horizontalalignment='center')
        if int(longVal[r]) > 0:
            ax.annotate(str(longVal[r]),
                        xy = (t[r], l[r] - padding),
                        xytext = (t[r], l[r] - padding),
                        color=td_setup_long_col,
                        size=10,weight='bold',
                        horizontalalignment='center')
        #insert arrows when setup completes
        if shortVal[r] == 9:
            plt.annotate('▼', xy=(t[r], h[r] + 2 * padding), xytext=(t[r], h[r] + 2 * padding),
                         color=td_setup_complete_short_col, horizontalalignment='center', verticalalignment='center', size=13)
        if longVal[r] == 9:
            plt.annotate('▲', xy=(t[r], h[r] - 2 * padding), xytext=(t[r], h[r] - 2 * padding),
                         color=td_setup_complete_long_col, horizontalalignment='center', verticalalignment='center', size=13)

    logging.info('整形中...')        
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ticks = plt.gca().get_xticklabels()
    for label in ticks:
        label.set_rotation(60) #units here are degrees
        label.set_fontsize(8)

    ax.set_title(r'light green/pink: setup ($\geq$ 9 implicates end of short-term trend)' + '\n' + 
                 r'dark green/red: countdown ($\geq$ 13 implicates end of long-term trend)');
    ax.set_ylim(min(l) - 0.1 * (max(h) - min(l)),
                max(h) + 0.1 * (max(h) - min(l)))
    plt.show()
    if savefigname is not None:
        fig.savefig(savefigname)
        