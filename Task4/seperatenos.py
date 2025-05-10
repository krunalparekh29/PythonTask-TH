def seperate_numbers(no_to_be_greater_than):
    numbers=list(range(1,1001))
    even_no_list=[]
    no_divisible_by_17=[]
    no_greater_than=[]
    for no in numbers:
        if no %2==0:
            even_no_list.append(no)
        if no %17==0:
            no_divisible_by_17.append(no)
        if no>=no_to_be_greater_than:
            no_greater_than.append(no)
    return even_no_list,no_divisible_by_17,no_greater_than


no_to_be_greater_than=int(input("Enter value to be greater than..."))
even_no_list,no_divisible_by_17,no_greater_than=seperate_numbers(no_to_be_greater_than)
print(even_no_list)
print(no_divisible_by_17)
print(no_greater_than)
