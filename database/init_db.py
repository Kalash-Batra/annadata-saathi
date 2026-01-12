import sqlite3
import json

def init_db():
    conn = sqlite3.connect('annadata_saathi.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS government_schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            crop TEXT NOT NULL,
            scheme_name TEXT NOT NULL,
            description TEXT,
            benefits TEXT,
            eligibility TEXT,
            how_to_apply TEXT,
            ministry TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            language TEXT,
            crop_category TEXT,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    schemes_data = [
        
        ('Maharashtra', 'Soybean', 'Pradhan Mantri Krishi Sinchai Yojana', 'Irrigation support scheme', 'Improved irrigation facilities', 'All farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Rice', 'National Food Security Mission', 'Increase rice productivity', 'Seed and input subsidy', 'Small and marginal farmers', 'Apply through state agriculture dept', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Cotton', 'Soil Health Card Scheme', 'Soil testing and nutrient advice', 'Free soil health card', 'All farmers', 'Apply at Krushi Seva Kendra', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Sugarcane', 'Micro Irrigation Fund Scheme', 'Water saving irrigation scheme', 'Drip irrigation subsidy', 'All farmers', 'Apply via state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Pulses', 'National Mission on Pulses', 'Increase pulse production', 'Seed and technology support', 'All farmers', 'Apply through agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Maize', 'Paramparagat Krishi Vikas Yojana', 'Organic farming promotion', 'Financial assistance for organic inputs', 'Farmers willing to adopt organic farming', 'Apply via PKVY portal', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Vegetables', 'Mission for Integrated Development of Horticulture', 'Horticulture development scheme', 'Subsidy for vegetables cultivation', 'All farmers', 'Apply through horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Groundnut', 'National Oilseeds Mission', 'Oilseed production support', 'Seed and fertilizer subsidy', 'All farmers', 'Apply through state agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'Fruits', 'Pradhan Mantri Krishi Sampada Yojana', 'Agri-processing infrastructure scheme', 'Cold storage and processing subsidy', 'Farmer producer organizations', 'Apply through MoFPI portal', 'MINISTRY OF AGRICULTURE'),
        ('Maharashtra', 'All Crops', 'Kisan Credit Card Scheme', 'Credit support for farmers', 'Low interest crop loans', 'All farmers', 'Apply through banks', 'MINISTRY OF AGRICULTURE'),
       

        ('Punjab', 'Wheat', 'National Food Security Mission', 'Increase wheat productivity', 'Seed and fertilizer subsidy', 'All farmers', 'Apply through agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Rice', 'Pradhan Mantri Krishi Sinchai Yojana', 'Irrigation support scheme', 'Subsidy for irrigation systems', 'All farmers', 'Apply via state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Maize', 'Paramparagat Krishi Vikas Yojana', 'Organic farming promotion', 'Financial support for organic inputs', 'Farmers adopting organic farming', 'Apply through PKVY portal', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Cotton', 'Technology Mission on Cotton', 'Cotton productivity enhancement', 'Improved seed and pest control support', 'Cotton farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Pulses', 'National Mission on Pulses', 'Pulses production support', 'Seed and training assistance', 'All farmers', 'Apply via agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Vegetables', 'Mission for Integrated Development of Horticulture', 'Horticulture development scheme', 'Subsidy for vegetable cultivation', 'All farmers', 'Apply through horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'All Crops', 'Kisan Credit Card Scheme', 'Credit support for farmers', 'Low-interest crop loans', 'All farmers', 'Apply through banks', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Sugarcane', 'Rashtriya Krishi Vikas Yojana', 'Agricultural development scheme', 'Subsidy for farm machinery', 'All farmers', 'Apply online on RKVY portal', 'MINISTRY OF AGRICULTURE'),
        ('Punjab', 'Oilseeds', 'National Oilseeds Mission', 'Oilseed production promotion', 'Seed and fertilizer subsidy', 'All farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),

        
        ('Uttar Pradesh', 'Rice', 'National Food Security Mission', 'Increase rice productivity', 'Seed and fertilizer assistance', 'All farmers', 'Apply through agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Wheat', 'PM-Kisan Scheme', 'Income support for farmers', '₹6000 per year in installments', 'All land-holding farmers', 'Register via PM-Kisan portal', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Sugarcane', 'Pradhan Mantri Krishi Sinchai Yojana', 'Irrigation support scheme', 'Subsidy for drip and sprinkler irrigation', 'All farmers', 'Apply through state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Potato', 'Soil Health Card Scheme', 'Soil testing and nutrient management', 'Free soil health card', 'All farmers', 'Contact Krushi Seva Kendra', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Maize', 'Paramparagat Krishi Vikas Yojana', 'Organic farming promotion', 'Financial assistance for organic inputs', 'Farmers adopting organic practices', 'Apply through PKVY portal', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Pulses', 'National Mission on Pulses', 'Increase pulse production', 'Seed and technical support', 'All farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Vegetables', 'Mission for Integrated Development of Horticulture', 'Horticulture development scheme', 'Subsidy for vegetable cultivation', 'All farmers', 'Apply through horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Oilseeds', 'National Oilseeds Mission', 'Oilseed production support', 'Seed and fertilizer subsidy', 'All farmers', 'Apply via agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'All Crops', 'Kisan Credit Card Scheme', 'Credit support for farmers', 'Low interest crop loans', 'All farmers', 'Apply through banks', 'MINISTRY OF AGRICULTURE'),
        ('Uttar Pradesh', 'Fruits', 'Pradhan Mantri Krishi Sampada Yojana', 'Post-harvest and processing scheme', 'Cold storage and processing subsidy', 'FPOs and farmer groups', 'Apply through MoFPI portal', 'MINISTRY OF AGRICULTURE'),
 
        
        ('Karnataka', 'Sugarcane', 'Pradhan Mantri Fasal Bima Yojana', 'Crop insurance scheme', 'Insurance coverage against crop loss', 'All farmers', 'Register through banks', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'Sugarcane', 'Pradhan Mantri Krishi Sinchai Yojana', 'Irrigation support scheme', 'Subsidy for drip irrigation', 'All farmers', 'Apply via state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'Coffee', 'National Mission on Sustainable Agriculture', 'Climate resilient agriculture', 'Financial assistance for sustainable practices', 'Coffee growers', 'Apply through Coffee Board', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'Coffee', 'Paramparagat Krishi Vikas Yojana', 'Organic farming promotion', 'Support for organic coffee farming', 'Farmers adopting organic methods', 'Apply via PKVY portal', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'Coconut', 'Pradhan Mantri Krishi Sinchai Yojana', 'Micro-irrigation support', 'Drip irrigation subsidy', 'All farmers', 'Apply through state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'Millets', 'National Mission on Nutri-Cereals', 'Millet promotion scheme', 'Input subsidy and MSP support', 'Millet farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'Vegetables', 'Mission for Integrated Development of Horticulture', 'Horticulture development scheme', 'Subsidy for vegetable farming', 'All farmers', 'Apply via horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'All Crops', 'Kisan Credit Card Scheme', 'Credit support for farmers', 'Low-interest agricultural loans', 'All farmers', 'Apply through banks', 'MINISTRY OF AGRICULTURE'),
        ('Karnataka', 'All Crops', 'Soil Health Card Scheme', 'Soil testing and nutrient management', 'Free soil health card', 'All farmers', 'Contact Krushi Seva Kendra', 'MINISTRY OF AGRICULTURE'),

        ('Tamil Nadu', 'Rice', 'PM-Kisan Scheme', 'Income support for farmers', '₹6000 per year in installments', 'All land-holding farmers', 'Apply via PM-Kisan portal', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Rice', 'National Food Security Mission', 'Increase rice productivity', 'Seed and fertilizer subsidy', 'All farmers', 'Apply through agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Cotton', 'Technology Mission on Cotton', 'Cotton productivity enhancement', 'Improved seeds and pest management support', 'Cotton farmers', 'Apply via agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Cotton', 'Soil Health Card Scheme', 'Soil testing and nutrient management', 'Free soil health card', 'All farmers', 'Apply at Krushi Seva Kendra', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Coconut', 'National Horticulture Mission', 'Horticulture development scheme', 'Subsidy for coconut cultivation', 'All farmers', 'Apply through horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Coconut', 'Pradhan Mantri Krishi Sinchai Yojana', 'Micro-irrigation support', 'Drip irrigation subsidy', 'All farmers', 'Apply via state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Millets', 'National Mission on Nutri-Cereals', 'Millet promotion scheme', 'Input subsidy and MSP support', 'Millet farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'Vegetables', 'Mission for Integrated Development of Horticulture', 'Horticulture development scheme', 'Subsidy for vegetable cultivation', 'All farmers', 'Apply through horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'All Crops', 'Kisan Credit Card Scheme', 'Credit support for farmers', 'Low-interest agricultural loans', 'All farmers', 'Apply through banks', 'MINISTRY OF AGRICULTURE'),
        ('Tamil Nadu', 'All Crops', 'Soil Health Card Scheme', 'Soil testing and nutrient management', 'Free soil health card', 'All farmers', 'Contact agriculture office', 'MINISTRY OF AGRICULTURE'),

        
        ('Telangana', 'Rice', 'PM-Kisan Scheme', 'Income support for farmers', '₹6000 per year in installments', 'All land-holding farmers', 'Apply via PM-Kisan portal', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Rice', 'National Food Security Mission', 'Increase rice productivity', 'Seed and fertilizer subsidy', 'All farmers', 'Apply through agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Cotton', 'Technology Mission on Cotton', 'Cotton productivity enhancement', 'Improved seeds and pest control support', 'Cotton farmers', 'Apply through agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Cotton', 'Soil Health Card Scheme', 'Soil testing and nutrient management', 'Free soil health card', 'All farmers', 'Apply at agriculture office', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Sugarcane', 'Pradhan Mantri Krishi Sinchai Yojana', 'Irrigation support scheme', 'Subsidy for drip and sprinkler irrigation', 'All farmers', 'Apply via state agriculture portal', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Sugarcane', 'Pradhan Mantri Fasal Bima Yojana', 'Crop insurance scheme', 'Coverage against crop loss', 'All farmers', 'Register through banks', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Pulses', 'National Mission on Pulses', 'Pulse production support', 'Seed and technical assistance', 'All farmers', 'Apply through agriculture department', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'Vegetables', 'Mission for Integrated Development of Horticulture', 'Horticulture development scheme', 'Subsidy for vegetable cultivation', 'All farmers', 'Apply through horticulture department', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'All Crops', 'Kisan Credit Card Scheme', 'Credit support for farmers', 'Low-interest crop loans', 'All farmers', 'Apply through banks', 'MINISTRY OF AGRICULTURE'),
        ('Telangana', 'All Crops', 'Soil Health Card Scheme', 'Soil testing and nutrient management', 'Free soil health card', 'All farmers', 'Contact agriculture office', 'MINISTRY OF AGRICULTURE'),
    ]

    
    cursor.execute('SELECT COUNT(*) FROM government_schemes')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO government_schemes (state, crop, scheme_name, description, benefits, eligibility, how_to_apply, ministry)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', schemes_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
