import data
from typing import Tuple, List, Any

# to convert the sql database to a dictionary format I can work with


def convertSQLTableToDictFormat(headerTuple: Tuple[str], rowList: List[Tuple[Any]]):
    result = []

    for rowTuple in rowList:
        rowDict = {}
        for i in range(len(headerTuple)):
            key = headerTuple[i]
            value = rowTuple[i]
            rowDict[key] = value

        result.append(rowDict)

    return result

# to get the corresponding values of a particular row using the unique id


def find_pu_result(list_of_dicts, target_value, key_to_check):
    keys_with_target_value = []

    for dic in list_of_dicts:
        for item, value in dic.items():
            if item == key_to_check and value == target_value:
                keys_with_target_value.append(dic)
    return keys_with_target_value

# stores new result to tha data in a case og adding more polling unit results


def store_new_result(result_id, unique_id, party_abr, party_score, user_name, date_entered, user_ip_adress):
    data_tuple = (result_id, unique_id, party_abr, party_score, user_name, date_entered, user_ip_adress)
    data.ANNOUNCED_PU_RESULTS_TABLE_ROWS.append(data_tuple)
    return data.ANNOUNCED_PU_RESULTS_TABLE_ROWS


# Number 1 solution. Prints out the result of any individual polling unit using the polling unit unique ID
pu_id = input("Please enter the polling unit unique ID\n")
pu_results = convertSQLTableToDictFormat(data.POLLING_UNIT_TABLE_HEADER,data.POLLING_UNIT_TABLE_ROWS)
result = find_pu_result(pu_results, int(pu_id), key_to_check='uniqueid')
for dictionary in result:
    print(f"Polling Unit data with unique {pu_id}: {dictionary}")


# Number 2 Solution. Prints out the total result of all PU in Delta State
print("The total result for all Polling Units in Delta State is: ")

polling_unit_result = convertSQLTableToDictFormat(data.ANNOUNCED_PU_RESULTS_TABLE_HEADER,
                                                  data.ANNOUNCED_PU_RESULTS_TABLE_ROWS)

party_score_result = {}
for i in range(len(polling_unit_result)):
    party = polling_unit_result[i]['party_abbreviation']
    score = polling_unit_result[i]['party_score']
    if party in party_score_result:
        party_score_result[party] += score
    else:
        party_score_result[party] = score
print(f"The summed total result for all the polling units of each party in all local governments in Delta "
      f"state is {party_score_result}")

# Prints out the total results for each polling unit with same unique id
print("The total results for each polling unit with same unique ID is: ")
unique_id_scores = {}
for row in data.ANNOUNCED_PU_RESULTS_TABLE_ROWS:
    _, unique_id, party_abbr, party_score, _, _, _ = row

    if unique_id in unique_id_scores:
        if party_abbr in unique_id_scores[unique_id]:
            unique_id_scores[unique_id][party_abbr] += party_score
        else:
            unique_id_scores[unique_id][party_abbr] = party_score
    else:
        unique_id_scores[unique_id] = {party_abbr: party_score}

for unique_id, scores in unique_id_scores.items():
    print(f"Unique ID: {unique_id}, Scores: {scores}")

enter_new_pu_result = True
while enter_new_pu_result:
    choice = input("Do you want to store in new results for a polling unit?\nType Y for Yes and N for no ").lower()
    if choice == 'n':
        enter_new_pu_result = False
    else:
        new_id = input("Insert result ID")
        new_unique_id = input("Insert result unique ID")
        new_party = input("Insert Party Name")
        new_score = input("Insert Party Score")
        name = input("Insert your name")
        new_date = input("Insert date entered")
        address = input("Insert your IP address")

        store_new_result(new_id, new_unique_id, new_party, new_score, name, new_date, address)


