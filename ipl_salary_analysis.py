"""
IPL Player Salary Analysis
A beginner-friendly data analysis project
 
What this does:
- Loads IPL player salary data
- Cleans and analyzes it
- Creates visualizations
- Answers business questions
 
Skills demonstrated: Data cleaning, analysis, visualization with Python
Author: Ayush Jha
"""
 
# Import libraries (tools we need)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
# Set style for prettier graphs
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
 
print("=" * 50)
print("IPL SALARY ANALYSIS DASHBOARD")
print("=" * 50)
 
# ============================================
# STEP 1: LOAD THE DATA
# ============================================
print("\n📊 Loading data...")
df = pd.read_csv('ipl_salary_analysis.csv')
 
print(f"✅ Loaded {len(df)} players")
print("\n👀 First look at the data:")
print(df.head())
 
# ============================================
# STEP 2: DATA CLEANING & EXPLORATION
# ============================================
print("\n" + "=" * 50)
print("🔍 DATA QUALITY CHECK")
print("=" * 50)
 
# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())
 
# Basic statistics
print("\n📈 Salary Statistics (in Crores):")
print(df['Salary_Crores'].describe())
 
# ============================================
# STEP 3: ANALYSIS & INSIGHTS
# ============================================
print("\n" + "=" * 50)
print("💡 KEY INSIGHTS")
print("=" * 50)
 
# Top 5 highest paid players
print("\n🏆 Top 5 Highest Paid Players:")
top_earners = df.nlargest(5, 'Salary_Crores')[['Player', 'Team', 'Salary_Crores']]
print(top_earners.to_string(index=False))
 
# Average salary by role
print("\n💰 Average Salary by Role:")
role_avg = df.groupby('Role')['Salary_Crores'].mean().sort_values(ascending=False)
print(role_avg)
 
# Most expensive team
print("\n🏏 Team with Highest Total Salary:")
team_salary = df.groupby('Team')['Salary_Crores'].sum().sort_values(ascending=False)
print(team_salary.head())
 
# Performance vs Salary for batsmen
batsmen = df[df['Role'] == 'Batsman'].copy()
batsmen['Runs_Per_Match'] = batsmen['Runs_Scored'] / batsmen['Matches_Played']
batsmen['Value_Score'] = batsmen['Runs_Per_Match'] / batsmen['Salary_Crores']
 
print("\n⚡ Best Value Batsmen (Performance vs Cost):")
best_value = batsmen.nlargest(5, 'Value_Score')[['Player', 'Salary_Crores', 'Runs_Per_Match', 'Value_Score']]
print(best_value.to_string(index=False))
 
# ============================================
# STEP 4: VISUALIZATIONS
# ============================================
print("\n" + "=" * 50)
print("📊 GENERATING VISUALIZATIONS")
print("=" * 50)
 
# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('IPL Player Salary Analysis Dashboard', fontsize=16, fontweight='bold')
 
# 1. Top 10 Highest Paid Players
ax1 = axes[0, 0]
top_10 = df.nlargest(10, 'Salary_Crores')
colors = sns.color_palette("rocket", len(top_10))
ax1.barh(top_10['Player'], top_10['Salary_Crores'], color=colors)
ax1.set_xlabel('Salary (Crores)', fontweight='bold')
ax1.set_title('Top 10 Highest Paid Players', fontweight='bold')
ax1.invert_yaxis()
 
# 2. Salary Distribution by Role
ax2 = axes[0, 1]
role_data = df.groupby('Role')['Salary_Crores'].mean().sort_values()
colors = sns.color_palette("viridis", len(role_data))
ax2.bar(role_data.index, role_data.values, color=colors)
ax2.set_ylabel('Average Salary (Crores)', fontweight='bold')
ax2.set_title('Average Salary by Role', fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
 
# 3. Age vs Salary Scatter Plot
ax3 = axes[1, 0]
scatter = ax3.scatter(df['Age'], df['Salary_Crores'], 
                     c=df['Salary_Crores'], cmap='coolwarm', 
                     s=100, alpha=0.6, edgecolors='black')
ax3.set_xlabel('Age', fontweight='bold')
ax3.set_ylabel('Salary (Crores)', fontweight='bold')
ax3.set_title('Age vs Salary Analysis', fontweight='bold')
plt.colorbar(scatter, ax=ax3, label='Salary')
 
# 4. Team-wise Total Salary
ax4 = axes[1, 1]
team_total = df.groupby('Team')['Salary_Crores'].sum().sort_values(ascending=False)
colors = sns.color_palette("mako", len(team_total))
ax4.bar(team_total.index, team_total.values, color=colors)
ax4.set_ylabel('Total Salary (Crores)', fontweight='bold')
ax4.set_title('Team-wise Total Salary Budget', fontweight='bold')
ax4.tick_params(axis='x', rotation=45)
 
plt.tight_layout()
plt.savefig('ipl_salary_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Dashboard saved as 'ipl_salary_dashboard.png'")
 
# Create additional analysis: Performance vs Salary
fig2, ax = plt.subplots(figsize=(12, 8))
 
# Batsmen performance vs salary
batsmen_plot = df[df['Role'] == 'Batsman'].copy()
batsmen_plot['Runs_Per_Match'] = batsmen_plot['Runs_Scored'] / batsmen_plot['Matches_Played']
 
scatter = ax.scatter(batsmen_plot['Salary_Crores'], 
                    batsmen_plot['Runs_Per_Match'],
                    s=batsmen_plot['Matches_Played']*2,
                    c=batsmen_plot['Age'],
                    cmap='plasma',
                    alpha=0.6,
                    edgecolors='black',
                    linewidth=1.5)
 
# Add player names to notable points
for idx, row in batsmen_plot.iterrows():
    if row['Salary_Crores'] > 15 or row['Runs_Per_Match'] > 35:
        ax.annotate(row['Player'], 
                   (row['Salary_Crores'], row['Runs_Per_Match']),
                   fontsize=9, 
                   xytext=(5, 5),
                   textcoords='offset points')
 
ax.set_xlabel('Salary (Crores)', fontsize=12, fontweight='bold')
ax.set_ylabel('Runs Per Match', fontsize=12, fontweight='bold')
ax.set_title('Batsmen: Are High Salaries Worth It?', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Age')
 
plt.tight_layout()
plt.savefig('performance_vs_salary.png', dpi=300, bbox_inches='tight')
print("✅ Performance analysis saved as 'performance_vs_salary.png'")
 
# ============================================
# STEP 5: EXPORT INSIGHTS TO EXCEL
# ============================================
print("\n📄 Exporting detailed analysis to Excel...")
 
with pd.ExcelWriter('ipl_salary_insights.xlsx', engine='openpyxl') as writer:
    # Sheet 1: Raw data
    df.to_excel(writer, sheet_name='Raw Data', index=False)
    
    # Sheet 2: Top performers
    top_earners_full = df.nlargest(10, 'Salary_Crores')
    top_earners_full.to_excel(writer, sheet_name='Top Earners', index=False)
    
    # Sheet 3: Role-wise analysis
    role_analysis = df.groupby('Role').agg({
        'Salary_Crores': ['mean', 'max', 'min', 'count'],
        'Age': 'mean'
    }).round(2)
    role_analysis.to_excel(writer, sheet_name='Role Analysis')
    
    # Sheet 4: Team-wise analysis
    team_analysis = df.groupby('Team').agg({
        'Salary_Crores': ['sum', 'mean', 'count'],
        'Age': 'mean'
    }).round(2)
    team_analysis.to_excel(writer, sheet_name='Team Analysis')
 
print("✅ Excel report saved as 'ipl_salary_insights.xlsx'")
 
# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 50)
print("✨ ANALYSIS COMPLETE!")
print("=" * 50)
print("\n📁 Files Created:")
print("1. ipl_salary_dashboard.png - Main visualization dashboard")
print("2. performance_vs_salary.png - Performance analysis")
print("3. ipl_salary_insights.xlsx - Detailed Excel report")
print("\n🎯 This project demonstrates:")
print("   ✓ Data loading and cleaning")
print("   ✓ Statistical analysis")
print("   ✓ Data visualization")
print("   ✓ Business insights generation")
print("   ✓ Excel reporting")
print("\n" + "=" * 50)
