# Script to update template paths in views.py

# Path to the views.py file
views_path = r'c:\App_Granja\avicola\views.py'

# Read the content of the file
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the template paths
updated_content = content.replace(
    "return render(request, 'core/dashboard.html', context)",
    "return render(request, 'avicola/dashboard_supervisor.html', context)",
    1  # Only replace the first occurrence (dashboard_supervisor)
)

updated_content = updated_content.replace(
    "return render(request, 'core/dashboard.html', context)",
    "return render(request, 'avicola/dashboard_operario.html', context)",
    1  # Only replace the next occurrence (dashboard_operario)
)

# Write the updated content back to the file
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Template paths updated successfully!")
