
def offensive_actions(ax, pname):
            # Viz Dfs:
            playerdf = df[df['name']==pname]
            passdf = playerdf[playerdf['type']=='Pass']
            succ_passdf = passdf[passdf['outcomeType']=='Successful']
            prg_pass = playerdf[(playerdf['prog_pass']>9.144) & (playerdf['outcomeType']=='Successful') & (playerdf['x']>35) &
                                (playerdf['type_value_Corner taken']!=6) & (playerdf['type_value_Free kick taken']!=5)]
            prg_carry = playerdf[(playerdf['prog_carry']>9.144) & (playerdf['endX']>35)]
            cc = playerdf[(playerdf['type_value_Assist']==210)]
            ga = playerdf[(playerdf['assist']==1)]
            goal = playerdf[(playerdf['type']=='Goal') & (playerdf['isOwnGoal'].isna())]
            owngoal = playerdf[(playerdf['type']=='Goal') & (playerdf['isOwnGoal'].notna())]
            ontr = playerdf[(playerdf['type']=='SavedShot')]
            oftr = playerdf[playerdf['type'].isin(['MissedShots', 'ShotOnPost'])]
            takeOns = playerdf[(playerdf['type']=='TakeOn') & (playerdf['outcomeType']=='Successful')]
            takeOnu = playerdf[(playerdf['type']=='TakeOn') & (playerdf['outcomeType']=='Unsuccessful')]

            # Pitch Plot
            pitch = VerticalPitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, line_zorder=2, linewidth=2, pad_bottom=27)
            pitch.draw(ax=ax)

            # line, arrow, scatter Plots
            pitch.lines(succ_passdf.x, succ_passdf.y, succ_passdf.endX, succ_passdf.endY, color='gray', comet=True, lw=2, alpha=0.65, zorder=1, ax=ax)
            pitch.scatter(succ_passdf.endX, succ_passdf.endY, color=bg_color, ec='gray', s=20, zorder=2, ax=ax)
            pitch.lines(prg_pass.x, prg_pass.y, prg_pass.endX, prg_pass.endY, color=col2, comet=True, lw=3, zorder=2, ax=ax)
            pitch.scatter(prg_pass.endX, prg_pass.endY, color=bg_color, ec=col2, s=40, zorder=3, ax=ax)
            pitch.lines(cc.x, cc.y, cc.endX, cc.endY, color=violet, comet=True, lw=3.5, zorder=3, ax=ax)
            pitch.scatter(cc.endX, cc.endY, color=bg_color, ec=violet, s=50, lw=1.5, zorder=4, ax=ax)
            pitch.lines(ga.x, ga.y, ga.endX, ga.endY, color='green', comet=True, lw=4, zorder=4, ax=ax)
            pitch.scatter(ga.endX, ga.endY, color=bg_color, ec='green', s=60, lw=2, zorder=5, ax=ax)

            for index, row in prg_carry.iterrows():
                arrow = patches.FancyArrowPatch((row['y'], row['x']), (row['endY'], row['endX']), arrowstyle='->', color=col2, zorder=2, mutation_scale=20, 
                                                linewidth=2, linestyle='--')
                ax.add_patch(arrow)

            pitch.scatter(goal.x, goal.y, c=bg_color, edgecolors='green', linewidths=1.2, s=300, marker='football', zorder=10, ax=ax)
            pitch.scatter(owngoal.x, owngoal.y, c=bg_color, edgecolors='orange', linewidths=1.2, s=300, marker='football', zorder=10, ax=ax)
            pitch.scatter(ontr.x, ontr.y, c=col1, edgecolors=line_color, linewidths=1.2, s=200, alpha=0.75, zorder=9, ax=ax)
            pitch.scatter(oftr.x, oftr.y, c=bg_color, edgecolors=col1, linewidths=1.2, s=200, alpha=0.75, zorder=8, ax=ax)

            pitch.scatter(takeOns.x, takeOns.y, c='orange', edgecolors=line_color, marker='h', s=200, alpha=0.75, zorder=7, ax=ax)
            pitch.scatter(takeOnu.x, takeOnu.y, c=bg_color, edgecolors='orange', marker='h', lw=1.2, hatch='//////', s=200, alpha=0.85, zorder=7, ax=ax)

            # Stats:
            pitch.scatter(-5, 68, c=bg_color, edgecolors='green', linewidths=1.2, s=300, marker='football', zorder=10, ax=ax)
            pitch.scatter(-10, 68, c=col1, edgecolors=line_color, linewidths=1.2, s=300, alpha=0.75, zorder=9, ax=ax)
            pitch.scatter(-15, 68, c=bg_color, edgecolors=col1, linewidths=1.2, s=300, alpha=0.75, zorder=8, ax=ax)
            pitch.scatter(-20, 68, c='orange', edgecolors=line_color, marker='h', s=300, alpha=0.75, zorder=7, ax=ax)
            pitch.scatter(-25, 68, c=bg_color, edgecolors='orange', marker='h', lw=1.2, hatch='//////', s=300, alpha=0.85, zorder=7, ax=ax)
            if len(owngoal)>0:
                ax_text(64, -4.5, f'Goals: {len(goal)} | <OwnGoal: {len(owngoal)}>', fontsize=12, highlight_textprops=[{'color':'orange'}], ax=ax)
            else:
                ax.text(64, -5.5, f'Goals: {len(goal)}', fontsize=12)
            ax.text(64, -10.5, f'Shots on Target: {len(ontr)}', fontsize=12)
            ax.text(64, -15.5, f'Shots off Target: {len(oftr)}', fontsize=12)
            ax.text(64, -20.5, f'TakeOn (Succ.): {len(takeOns)}', fontsize=12)
            ax.text(64, -25.5, f'TakeOn (Unsucc.): {len(takeOnu)}', fontsize=12)

            pitch.lines(-5, 34, -5, 24, color='gray', comet=True, lw=2, alpha=0.65, zorder=1, ax=ax)
            pitch.scatter(-5, 24, color=bg_color, ec='gray', s=20, zorder=2, ax=ax)
            pitch.lines(-10, 34, -10, 24, color=col2, comet=True, lw=3, zorder=2, ax=ax)
            pitch.scatter(-10, 24, color=bg_color, ec=col2, s=40, zorder=3, ax=ax)
            arrow = patches.FancyArrowPatch((34, -15), (23, -15), arrowstyle='->', color=col2, zorder=2, mutation_scale=20, 
                                                linewidth=2, linestyle='--')
            ax.add_patch(arrow)
            pitch.lines(-20, 34, -20, 24, color=violet, comet=True, lw=3.5, zorder=3, ax=ax)
            pitch.scatter(-20, 24, color=bg_color, ec=violet, s=50, lw=1.5, zorder=4, ax=ax)
            pitch.lines(-25, 34, -25, 24, color='green', comet=True, lw=4, zorder=4, ax=ax)
            pitch.scatter(-25, 24, color=bg_color, ec='green', s=60, lw=2, zorder=5, ax=ax)

            ax.text(21, -5.5, f'Successful Pass: {len(succ_passdf)}', fontsize=12)
            ax.text(21, -10.5, f'Porgressive Pass: {len(prg_pass)}', fontsize=12)
            ax.text(21, -15.5, f'Porgressive Carry: {len(prg_carry)}', fontsize=12)
            ax.text(21, -20.5, f'Key Passes: {len(cc)}', fontsize=12)
            ax.text(21, -25.5, f'Assists: {len(ga)}', fontsize=12)

            ax.text(34, 110, 'Offensive Actions', fontsize=20, fontweight='bold', ha='center', va='center')
            return
        

def pass_receiving_and_touchmap(ax, pname):
            # Viz Dfs:
            playerdf = df[df['name']==pname]
            touch_df = playerdf[(playerdf['x']>0) & (playerdf['y']>0)]
            pass_rec = df[(df['type']=='Pass') & (df['outcomeType']=='Successful') & (df['name'].shift(-1)==pname)]
            # touch_df = pd.concat([acts_df, pass_rec], ignore_index=True)
            actual_touch = playerdf[playerdf['isTouch']==1]

            fthd_tch = actual_touch[actual_touch['x']>=70]
            penbox_tch = actual_touch[(actual_touch['x']>=88.5) & (actual_touch['y']>=13.6) & (actual_touch['y']<=54.4)]

            fthd_rec = pass_rec[pass_rec['endX']>=70]
            penbox_rec = pass_rec[(pass_rec['endX']>=88.5) & (pass_rec['endY']>=13.6) & (pass_rec['endY']<=54.4)]

            pitch = VerticalPitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2, pad_bottom=27)
            pitch.draw(ax=ax)

            ax.scatter(touch_df.y, touch_df.x, marker='o', s=30, c='None', edgecolor=col2, lw=2)
            if len(touch_df)>3:
                # Calculate mean point
                mean_point = np.mean(touch_df[['y', 'x']].values, axis=0)
                
                # Calculate distances from the mean point
                distances = np.linalg.norm(touch_df[['y', 'x']].values - mean_point[None, :], axis=1)
                
                # Compute the interquartile range (IQR)
                q1, q3 = np.percentile(distances, [20, 80])  # Middle 75%: 12.5th to 87.5th percentile
                iqr_mask = (distances >= q1) & (distances <= q3)
                
                # Filter points within the IQR
                points_within_iqr = touch_df[['y', 'x']].values[iqr_mask]
                
                # Check if we have enough points for a convex hull
                if len(points_within_iqr) >= 3:
                    hull = ConvexHull(points_within_iqr)
                    for simplex in hull.simplices:
                        ax.plot(points_within_iqr[simplex, 0], points_within_iqr[simplex, 1], color=col2, linestyle='--')
                    ax.fill(points_within_iqr[hull.vertices, 0], points_within_iqr[hull.vertices, 1], 
                            facecolor='none', edgecolor=col2, alpha=0.3, hatch='/////', zorder=1)
                else:
                    pass
            else:
                pass

            ax.scatter(pass_rec.endY, pass_rec.endX, marker='o', s=30, c='None', edgecolor=col1, lw=2)
            if len(touch_df)>4:
                # Calculate mean point
                mean_point = np.mean(pass_rec[['endY', 'endX']].values, axis=0)
                
                # Calculate distances from the mean point
                distances = np.linalg.norm(pass_rec[['endY', 'endX']].values - mean_point[None, :], axis=1)
                
                # Compute the interquartile range (IQR)
                q1, q3 = np.percentile(distances, [25, 75])  # Middle 75%: 12.5th to 87.5th percentile
                iqr_mask = (distances >= q1) & (distances <= q3)
                
                # Filter points within the IQR
                points_within_iqr = pass_rec[['endY', 'endX']].values[iqr_mask]
                
                # Check if we have enough points for a convex hull
                if len(points_within_iqr) >= 3:
                    hull = ConvexHull(points_within_iqr)
                    for simplex in hull.simplices:
                        ax.plot(points_within_iqr[simplex, 0], points_within_iqr[simplex, 1], color=col1, linestyle='--')
                    ax.fill(points_within_iqr[hull.vertices, 0], points_within_iqr[hull.vertices, 1], 
                            facecolor='none', edgecolor=col1, alpha=0.3, hatch='/////', zorder=1)
                else:
                    pass
            else:
                pass

            ax_text(34, 110, '<Touches> & <Pass Receiving> Points', fontsize=20, fontweight='bold', ha='center', va='center', 
                    highlight_textprops=[{'color':col2}, {'color':col1}])
            ax.text(34, -5, f'Total Touches: {len(actual_touch)} | at Final Third: {len(fthd_tch)} | at Penalty Box: {len(penbox_tch)}', color=col2, fontsize=13, ha='center', va='center')
            ax.text(34, -9, f'Total Pass Received: {len(pass_rec)} | at Final Third: {len(fthd_rec)} | at Penalty Box: {len(penbox_rec)}', color=col1, fontsize=13, ha='center', va='center')
            ax.text(34, -17, '*blue area = middle 75% touches area', color=col2, fontsize=13, fontstyle='italic', ha='center', va='center')
            ax.text(34, -21, '*red area = middle 75% pass receiving area', color=col1, fontsize=13, fontstyle='italic', ha='center', va='center')
            return
        

def defensive_actions(ax, pname):
            # Viz Dfs:
            playerdf = df[df['name']==pname]
            tackles = playerdf[(playerdf['type']=='Tackle') & (playerdf['outcomeType']=='Successful')]
            tackleu = playerdf[(playerdf['type']=='Tackle') & (playerdf['outcomeType']=='Unsuccessful')]
            ballrec = playerdf[playerdf['type']=='BallRecovery']
            intercp = playerdf[playerdf['type']=='Interception']
            clearnc = playerdf[playerdf['type']=='Clearance']
            passbkl = playerdf[playerdf['type']=='BlockedPass']
            shotbkl = playerdf[playerdf['type']=='Save']
            chalnge = playerdf[playerdf['type']=='Challenge']
            aerialw = playerdf[(playerdf['type']=='Aerial') & (playerdf['outcomeType']=='Successful')]
            aerialu = playerdf[(playerdf['type']=='Aerial') & (playerdf['outcomeType']=='Unsuccessful')]

            # Pitch Plot
            pitch = VerticalPitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2, pad_bottom=27)
            pitch.draw(ax=ax)

            # Scatter Plots
            sns.scatterplot(x=tackles.y, y=tackles.x, marker='X', s=300, color=col2, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            sns.scatterplot(x=tackleu.y, y=tackleu.x, marker='X', s=300, color=col1, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            pitch.scatter(ballrec.x, ballrec.y, marker='o', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(intercp.x, intercp.y, marker='*', lw=1.25, s=600, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(clearnc.x, clearnc.y, marker='h', lw=1.5, s=400, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(passbkl.x, passbkl.y, marker='s', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(shotbkl.x, shotbkl.y, marker='s', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(chalnge.x, chalnge.y, marker='+', lw=5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(aerialw.x, aerialw.y, marker='^', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(aerialu.x, aerialu.y, marker='^', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)

            # Stats
            sns.scatterplot(x=[65], y=[-5], marker='X', s=300, color=col2, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            sns.scatterplot(x=[65], y=[-10], marker='X', s=300, color=col1, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            pitch.scatter(-15, 65, marker='o', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-20, 65, marker='*', lw=1.25, s=600, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-25, 65, marker='h', lw=1.5, s=400, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            
            pitch.scatter(-5, 26, marker='s', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-10, 26, marker='s', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-15, 26, marker='+', lw=5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-20, 26, marker='^', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-25, 26, marker='^', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)

            ax.text(60, -5.5, f'Tackle (Succ.): {len(tackles)}', fontsize=12)
            ax.text(60, -10.5, f'Tackle (Unsucc.): {len(tackleu)}', fontsize=12)
            ax.text(60, -15.5, f'Ball Recoveries: {len(ballrec)}', fontsize=12)
            ax.text(60, -20.5, f'Interceptions: {len(intercp)}', fontsize=12)
            ax.text(60, -25.5, f'Clearance: {len(clearnc)}', fontsize=12)

            ax.text(21, -5.5, f'Passes Blocked: {len(passbkl)}', fontsize=12)
            ax.text(21, -10.5, f'Shots Blocked: {len(shotbkl)}', fontsize=12)
            ax.text(21, -15.5, f'Dribble Past: {len(chalnge)}', fontsize=12)
            ax.text(21, -20.5, f'Aerials Won: {len(aerialw)}', fontsize=12)
            ax.text(21, -25.5, f'Aerials Lost: {len(aerialu)}', fontsize=12)

            ax.text(34, 110, 'Defensive Actions', fontsize=20, fontweight='bold', ha='center', va='center')
            return
        
