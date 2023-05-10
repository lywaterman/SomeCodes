from paperqa import Docs

my_doc = ["/Users/ly/Documents/GitHub/SomeCodes/docs/isp.txt"]

docs = Docs(llm='gpt-3.5-turbo')
for d in my_doc:
    docs.add(d) 

while True:
    question = input("请输入问题：")
    if question == "exit":
        break
    answer = docs.query("请用中文回答这个问题，"+question)
    print(answer.answer)