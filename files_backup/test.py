
s="HOW TO CREATE DCO READY CREATIVE MASTERS"
found=0
def search(s,data):
    if("questions" in data.keys()):
        keys=data['questions'].keys()
        if(s in keys):
            found=1
            return
        else:
            for i in keys:
                search(s,data["questions"][i])
    else:
        #reached the end
        return

q=set({})
def questions(data):
    if("questions" in data.keys()):
        keys=data['questions'].keys()
        for i in keys:
            q.add(i)
            questions(data["questions"][i])

    elif("answer" in data.keys()):
        return

# search(s,data)
# if(found==0):
#     print("Not found")

# questions(data)
# print(q)
q={'Adobe After Effects - Advanced features', 'What is a Creative Master', 'What are Assets', 'Vector Shape Colors', 'Google Web Designer - Setup', 'How to update the Asset Source', 'Adding New Asset Source', 'Creative Master Guidelines - Custom HTML/Other Tools', 'Personalized Dynamic Creative - Visual Workflow', 'Jivox Creative Master Export Setup (For DCS Support)', 'HOW TO CREATE DCO READY CREATIVE MASTERS', 'Adobe After Effects - Setup', 'Uploading the Asset Source', 'Asset Sources', 'Adobe Animate - Setup', 'Deleting the Asset source', 'What are Creative Variations', 'Google Web Designer - Custom Fonts '}
