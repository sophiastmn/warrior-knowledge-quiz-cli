import random;
#####################  NOTE: This program depends on your file being in the following format:  #####################
#####################  ###1###                                                                 #####################
#####################  <<insert question 1 here>>////<<insert answer here>>                    #####################
#####################  Warrior knowledge blocks are separated by ###<<warrior knowledge block number>>###  #########

def randomKnowledge(questions, answers):
    #generate random knowledge: returns question and answer
    focusNum = random.randint(0, len(questions)-1);
    num = random.randint(0, len(questions[focusNum])-1);
    return questions[focusNum][num], answers[focusNum][num];

def fixText(text):
    #fix the text up
    text = ''.join([t for t in text if t not in ",.;'-/?! "]).upper();
    text = text.replace("FOURTH", "4TH");
    text = text.replace("THIRD", "3RD");
    text = text.replace("SECOND", "2ND");
    text = text.replace("FIRST", "1ST");
    return text;

def findWarriorKnowledgeRange(focusAreas):
    focusAreas = focusAreas.strip().replace(" ", "");
    #take input and turn it into an array
    if focusAreas.upper() == "A":
        return [*range(20)];
    #turn it into a series of ranges
    ranges = focusAreas.split(",");
    listOfKnowledge = [];
    for r in ranges:
        if r.find("-") < 0:
            listOfKnowledge.append(int(r));
        else:
            temp = [*range(int(r[:r.index("-")]), int(r[r.index("-")+1:])+1)];
            for t in temp:
                listOfKnowledge.append(int(t));
    return listOfKnowledge;
            

def retrieveAndParseQuestions(fileName, focusAreas):
    #take the input and output 2 arrays one with the questions, one with the answers

    #open questions file and separate questions and answers
    questions = [];
    answers = [];
    currKnowledge = -1;
    for line in open(fileName):
        strippedLine = line.strip();
        if strippedLine[:3] == "###":
            currKnowledge += 1;
            questions.append([]);
            answers.append([]);
        else:
            questions[currKnowledge].append(strippedLine[:strippedLine.index("////")]);
            answers[currKnowledge].append(strippedLine[strippedLine.index("////")+4:]);

    #find the Warrior Block knowledge areas of focus
    focuses = findWarriorKnowledgeRange(focusAreas);

    #only keep relevant questions
    qs = [];
    ans = [];
    for i, q in enumerate(questions):
        if i+1 in focuses:
            qs.append(q);
            ans.append(answers[i]);
    return qs, ans;

def main():
    #get some information from the user
    print("Welcome. Let's test your warrior knowledge!");
    questionsFile = input("What is the file name for your questions?: ");
    focusAreas = input("What blocks would you like to focus on? Enter a for all. Answers can be comma-separated and ranges can be indicated by a dash: ");
    print("Enter e to escape. Enter + before your next answer if your previous answer was incorrectly marked false. Type skip to skip a question.");
    points = 0;
    pointsPossible = 0;
    questions, answers = retrieveAndParseQuestions(questionsFile, focusAreas);

    answer = "";

    while (answer != "e"):
        pointsPossible += 1;
        q, a = randomKnowledge(questions, answers);
        answer = input(q+": ");
        if answer == "e":
            pointsPossible -= 1;
            break;
        if answer == "skip":
            pointsPossible -= 1;
            continue;
        if "+" in answer:
            points += 1;
            answer = answer.replace("+", "");
        if fixText(answer) == fixText(a):
            print("Correct");
            points += 1;
        else:
            print(f"Incorrect. The correct answer is: {a}");
            answer = input(q+": ");
            while fixText(answer) != fixText(a):
                print(f"Incorrect. The correct answer is: {a}");
                answer = input(q+": ");
            print(f"Correct. You may proceed.");
    print(f"Thanks for testing your knowledge!\n You scored: {points} out of {pointsPossible}, giving you an accuracy of {[(points/pointsPossible)*100 if pointsPossible > 0 else 0][0]}%");


if __name__=="__main__":
    main();
