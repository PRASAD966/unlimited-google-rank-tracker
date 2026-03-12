from database import get_db_connection

def recover_project_names():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Find all runs with 'nan' project name
    cursor.execute("SELECT id, target_domain FROM runs WHERE project_name = 'nan' OR project_name IS NULL OR project_name = ''")
    corrupted_runs = cursor.fetchall()
    
    print(f"Found {len(corrupted_runs)} corrupted runs.")
    
    # 2. Build a map of Domain -> Last Known Good Project Name
    cursor.execute("SELECT target_domain, project_name FROM runs WHERE project_name != 'nan' AND project_name != 'No Project' AND project_name IS NOT NULL AND project_name != '' ORDER BY id DESC")
    good_runs = cursor.fetchall()
    
    domain_map = {}
    for r in good_runs:
        d = r['target_domain']
        if d not in domain_map:
            domain_map[d] = r['project_name']
            
    print("Recovery Map:", domain_map)
    
    # 3. Update corrupted runs
    updated_count = 0
    for run in corrupted_runs:
        run_id = run['id']
        domain = run['target_domain']
        
        new_name = domain_map.get(domain, "Default Project")
        
        # If we have a good name, use it. If not, use 'Default Project' or maybe strictly the domain name but cleaned up?
        # User dislikes URL. Let's try to capitalize the domain.
        if not domain:
            new_name = "Recovered Project"
        elif new_name == "Default Project":
             # flipkart.com -> Flipkart
             clean_name = domain.replace("https://", "").replace("http://", "").replace("www.", "").split(".")[0].capitalize()
             new_name = f"{clean_name} Project"

        print(f"Recovering Run {run_id} ({domain}) -> {new_name}")
        cursor.execute("UPDATE runs SET project_name = %s WHERE id = %s", (new_name, run_id))
        updated_count += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully recovered {updated_count} runs.")

if __name__ == "__main__":
    recover_project_names()
