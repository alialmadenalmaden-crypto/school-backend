with open(r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\sections\institutes_list_section.dart", "r", encoding="utf-8") as f:
    content = f.read()

if "String getFormattedImageUrl" in content or "getFormattedImageUrl(" in content:
    print("Found getFormattedImageUrl in institutes_list_section.dart")
    # Print the definition of it
    idx = content.find("String getFormattedImageUrl")
    if idx != -1:
        print(content[idx:idx+400])
    else:
        print("Function signature 'String getFormattedImageUrl' NOT found. It might be imported!")
        # Let's print all imports
        for line in content.split('\n'):
            if line.startswith('import '):
                print(line)
