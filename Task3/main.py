

def user_data():
    people={}
    num_of_users=int(input("No of users to...."))
    for i in range(num_of_users):
        name=input("enter name")
        age=int(input("Enter age"))
        people[name]=age

    return people

def categorize_age_groups(people):
    age_groups={
        "18-35":[],
        "36-50":[],
        "51-65":[],
        "66-90":[]
    }

    for name,age in people.items():
        if 18<=age<=35:
           age_groups["18-35"].append((name,age))
        if 36 <= age <= 50:
           age_groups["36-50"].append((name, age))
        if 51<=age<=65:
           age_groups["51-65"].append((name,age))
        if 66<=age<=90:
           age_groups["66-90"].append((name,age))

    return age_groups

def maximum_minimum_person_in_each_group(age_groups):
    result={}
    for group, people in age_groups.items():
        if people:
            max_person = max(people, key=lambda x: x[1])
            min_person = min(people, key=lambda x: x[1])
            result[group] = {"maximum": max_person, "minimum": min_person}
        else:
            result[group] = {"max": None, "min": None}

    return result


def minimum_person_groups(age_groups):
    return age_groups["18-35"]


user_data=user_data()
age_segregation=categorize_age_groups(user_data)
age_extremes = maximum_minimum_person_in_each_group(age_segregation)
print(age_extremes)
