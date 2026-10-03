import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime, timedelta
import random

# --- ULTRA PRO STYLE ---
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'DejaVu Sans'

# DATA
np.random.seed(42)
n = 1200
categories = ['Furniture', 'Office Supplies', 'Technology']
sub_cats = {'Furniture': ['Chairs', 'Tables', 'Bookcases'], 'Office Supplies': ['Paper', 'Storage', 'Binders'], 'Technology': ['Phones', 'Accessories', 'Copiers']}
regions = ['West', 'East', 'Central', 'South']
data = []
start_date = datetime(2022, 1, 1)
for i in range(n):
    cat = random.choice(categories)
    sales = round(np.random.lognormal(6.5, 0.7), 2)
    data.append({'Order Date': start_date + timedelta(days=random.randint(0, 900)), 'Category': cat, 'Sub-Category': random.choice(sub_cats[cat]), 'Region': random.choice(regions), 'Sales': sales, 'Profit': round(sales * np.random.uniform(0.05, 0.4), 2), 'Quantity': random.randint(1, 10), 'Discount': random.choice([0, 0.1, 0.2])})
df = pd.DataFrame(data)
df['Month'] = pd.to_datetime(df['Order Date']).dt.to_period('M').astype(str)
monthly = df.groupby('Month')['Sales'].sum()
cat_sales = df.groupby('Category')['Sales'].sum()
region_sales = df.groupby('Region')['Sales'].sum().sort_values()
top_sub = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(6)

# --- DASHBOARD ---
fig = plt.figure(figsize=(18, 10), facecolor='#0E1117')
gs = gridspec.GridSpec(3, 3, hspace=0.4, wspace=0.3)

# KPI CARDS
fig.text(0.05, 0.92, f"RETAIL SALES DASHBOARD | Total Revenue: ${df['Sales'].sum():,.0f} | Total Profit: ${df['Profit'].sum():,.0f} | Orders: {n} | Avg Margin: {(df['Profit'].sum()/df['Sales'].sum()*100):.1f}%", fontsize=13, color='white', fontweight='bold', bbox=dict(facecolor='#1F77B4', alpha=0.8, boxstyle='round,pad=0.5'))

# 1. TREND
ax1 = fig.add_subplot(gs[0, :2], facecolor='#0E1117')
ax1.plot(monthly.index, monthly.values, color='#00D1FF', linewidth=3, marker='o', markersize=4)
ax1.fill_between(monthly.index, monthly.values, color='#00D1FF', alpha=0.15)
ax1.set_title('Monthly Sales Trend (Growth Analysis)', color='white', fontsize=12, fontweight='bold', loc='left')
ax1.tick_params(colors='gray', labelsize=8)
ax1.set_xticklabels(monthly.index, rotation=45, ha='right', fontsize=7)
for spine in ax1.spines.values(): spine.set_color('#333')

# 2. DONUT - Category
ax2 = fig.add_subplot(gs[0, 2], facecolor='#0E1117')
wedges, texts, autotexts = ax2.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%', colors=['#00D1FF', '#FF4B4B', '#00FF88'], wedgeprops={'edgecolor':'#0E1117','width':0.5}, textprops={'color':'white','fontsize':9})
ax2.set_title('Revenue by Category', color='white', fontsize=12, fontweight='bold', loc='left')

# 3. H-BAR - Region
ax3 = fig.add_subplot(gs[1, 0], facecolor='#0E1117')
ax3.barh(region_sales.index, region_sales.values, color=['#FF4B4B','#FF9F1C','#00FF88','#00D1FF'])
ax3.set_title('Region Performance', color='white', fontsize=12, fontweight='bold', loc='left')
ax3.tick_params(colors='gray')
for i, v in enumerate(region_sales.values): ax3.text(v+500, i, f"${v:,.0f}", color='white', va='center', fontsize=9)

# 4. V-BAR - Sub-Category
ax4 = fig.add_subplot(gs[1, 1:], facecolor='#0E1117')
bars = ax4.bar(top_sub.index, top_sub.values, color=plt.cm.cool(np.linspace(0,1,len(top_sub))), edgecolor='white', linewidth=0.5)
ax4.set_title('Top 6 Sub-Categories - Revenue Leaders', color='white', fontsize=12, fontweight='bold', loc='left')
ax4.tick_params(colors='gray', labelsize=9)
ax4.set_xticklabels(top_sub.index, rotation=15, ha='right')
for bar in bars: ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+200, f"${bar.get_height():,.0f}", ha='center', color='white', fontsize=8)

# 5. SCATTER - Profit vs Sales
ax5 = fig.add_subplot(gs[2, 0], facecolor='#0E1117')
scatter = ax5.scatter(df['Sales'], df['Profit'], c=df['Discount']*100, cmap='cool', alpha=0.6, s=df['Quantity']*15)
ax5.set_title('Profit vs Sales (Size=Qty, Color=Discount%)', color='white', fontsize=11, fontweight='bold', loc='left')
ax5.set_xlabel('Sales', color='gray'); ax5.set_ylabel('Profit', color='gray')
ax5.tick_params(colors='gray')
cbar = plt.colorbar(scatter, ax=ax5); cbar.ax.yaxis.set_tick_params(color='white'); cbar.set_label('Discount %', color='white')

# 6. INSIGHTS BOX
ax6 = fig.add_subplot(gs[2, 1:], facecolor='#0E1117')
ax6.axis('off')
best_month = monthly.idxmax(); best_region = region_sales.idxmax(); best_cat = cat_sales.idxmax()
insights_text = f"""
KEY INSIGHTS FOR MANAGEMENT:

1. Peak Sales Month: {best_month} (${monthly.max():,.0f}) - Festival Season Impact
2. Top Region: {best_region} leads with ${region_sales.max():,.0f} - Focus expansion here
3. Leading Category: {best_cat} - {cat_sales.max()/cat_sales.sum()*100:.1f}% of total revenue
4. Profitability: Average margin {(df['Profit'].sum()/df['Sales'].sum()*100):.1f}% - Maintain discount <20%
5. Growth Opportunity: Office Supplies needs promotion - lowest share
6. Recommendation: Increase stock for {top_sub.index[0]} & {top_sub.index[1]}

Next Action: Q4 Inventory Planning Based on Trend
"""
ax6.text(0, 0.9, insights_text, fontsize=11, color='#E0E0E0', va='top', fontfamily='monospace', bbox=dict(facecolor='#1C2128', edgecolor='#30363D', boxstyle='round,pad=0.8'))

plt.savefig('PROFESSIONAL_DASHBOARD.png', dpi=300, facecolor='#0E1117', bbox_inches='tight')
plt.show()
print("DONE - PROFESSIONAL_DASHBOARD.png saved - HD Quality!")