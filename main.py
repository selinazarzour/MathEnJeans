#Decembre 2021
def all_possibilities(c,n,arr):
  #c: nombre de couleurs
  #n: nombre de côtés
  #Cette fonction nous donne tous les possibilités différentes d'un octaèdre (8 faces) à c couleurs
  total_rows = c**n
  #On va remplir the matrix verticallement pour chaque colonne en passant par les lignes.
  for j in range (n):
    couleur = 0
    increment = c**j # seuil d'ajout
    repeat = c**(j+1)# seuil de repetition, reset
    for i in range(total_rows):
      if i%increment==0:
        if i%repeat==0:
          #Repeat every c^j+1, e.g 3^2
          #Reset the color to 0
          couleur = 0
        else:
          #Increment the color by 1 every 3^j e.g 3^1
          couleur+=1
      arr[i][j]=couleur
  print ("Total number of possibilities", total_rows)
  return

# We're not using this function
def validate_v2(row,c,n):
  couleur = 0
  found = False
  while (couleur < c and not found):
    j = 0
    while (j < n and not found):
      if (row[j] == couleur):
        found = True
        print ("found:",found, couleur,j)
      else:
        j+=1
    if found:
      couleur+=1 # Continue with the next color
      if couleur < c:   
        found = False # Check for new color
    else:
      couleur = c
  return found  

#fonction qui dit si la liste (row) est valide (tous les couleurs sont présentes) ou non
def validate(row,c,n):
  # This function will return True if the row includes all colors otherwise it will return False
  couleur = 0
  found = True
  # For each color, verify the color included at least once in the array. If not, return False.
  while (couleur<c and found):
    j = 0
    found = False
    while (j<n) and (not found):
      if row[j] == couleur:
        found = True
      else:
        j+=1
    couleur+=1
  return found

#Fonction qui crée les nouvelle listes (row) valides
# Count the rows that include all colors "valid" and put all valid rows in the new 2D array
def create_valid_arr(c,n,array_in):
  valid_count=0
  non_valid_count=0
  valid_array = []
  for row in array_in:
    if validate(row,c,n):
      valid_count+=1
      valid_array.append(row) # Row includes all colors so it's valid
    else:
      non_valid_count+=1

  print("Number of valid rows", valid_count)
  print("Number of discarded rows",non_valid_count)
  # print ("new non_dup_array\n", non_dup_array)
  return valid_array

def mirroring_row(row):
  size_row = len(row)
  #print("row size",size_row)
  row2 = [0 for i in range(size_row)]
  #print("row2:", row2)
  for j in range(size_row):
    #print(j,size_row-j-1)
    row2[j]=row[size_row-j-1]
  #print("row2",row2)
  return row2

def circular_shift_left(row,n):
  new_row = [0 for i in range(n)]
  new_row[0]=row[n-1]
  for j in range (n-1):
    new_row[j+1]=row[j]
  #print("new row shifted left by 1",new_row)
  return new_row

#Go through the valid 2D array and detect duplicate
def duplicate_row(row1,row2):
  # Verify if row1 match with row2 or any circular shift of it, Return True. Else, it's not the same pattern and return False
  # print ("row size", row_size)
  match = False
  counter = 0 # number of times to perform the shift max = n-1
  row3 = row2
  while (not match and counter < len(row1)):
    if row1 == row3:
      match = True
    else:
      row3 = circular_shift_left(row3,len(row3))
      counter+=1
  return match

def duplicate_array(row,arr):
  array_size = len(arr)
  # print ("array size", array_size)
  found = False
  counter = 0
  mirror_row = mirroring_row(row)
  while ((not found) and (counter < array_size)):
    if duplicate_row(row,arr[counter]) or duplicate_row(mirror_row,arr[counter]):
      # print("Found duplicate",counter)
      found = True
    else:
      counter+=1
  return found
  
def remove_duplicates(valid_array):
  res_array = [] # New array to build a table
  size_of_valid_array = len(valid_array)
  res_array.append(valid_array[0])
  for i in range (1, size_of_valid_array):
    if not duplicate_array(valid_array[i],res_array):
      # print ("non duplicate", valid_array[i])
      res_array.append(valid_array[i])
      # print (valid_array[i], file=open("output.txt", "a"))
      # print (".", file=open("output.txt", "a")) # show loading
      # print (valid_array[i], file=open("output.txt", "a"))
  return res_array

# Create list of all possible duplicates by swaping each 2 consecutive side starting from the second side [1] - Amendment 2 to the project but did not lead us to correct results
def known_duplicate(any_array):
  res_known_duplicate_array_list = [] #New array
  size_of_any_array = len(any_array)
  res_known_duplicate_array_list.append(any_array)
  for i in range(1,size_of_any_array):
    new_arr = [0 for i in range(size_of_any_array)]
    j=0
    while(j<size_of_any_array-1):
      if (i==j):
        new_arr[j] = any_array[j+1]
        new_arr[j+1] = any_array[j]
        j=j+1
      else:
        new_arr[j] = any_array[j]
      j=j+1
    res_known_duplicate_array_list.append(new_arr)
  #print("res_known_duplicate_array_list=",res_known_duplicate_array_list)
  return(res_known_duplicate_array_list)

def remove_duplicates_recursive(array,i):
  res_array = [] # New array to build a table
  res_array.append(array[i])
  counter = 1
  print("new count",len(array))
  #print("res array", res_array)
  res_known_duplicate_list = known_duplicate(array[i])
  j=i+1
  while(j<len(array)): 
    if not duplicate_array(array[j],res_known_duplicate_list):
      #print ("non duplicate", array[j])
      res_array.append(array[j])
      counter=counter+1
    j=j+1  
  i=i+1
  print("indicateur,new list length,previous list length",i,counter,j)
  if (i<counter):
    print("calling myself..")
    remove_duplicates_recursive(res_array,i)
  else:
    print("finished cleaning duplicate...",res_array)
    print("total:", len(res_array))
  return res_array

# Amemdment 3 to the project which we hope will lead us to accurate results
def array2matrix(row):
  matrix = [[0 for i in range(4)] for j in range(2)]
  for i in range (0,4):
    matrix[0][i]=row[i] 
  j=0
  for i in range (4,8):
    matrix[1][j]=row[i]
    j=j+1
  return matrix

def array2matrixPattern2(row):
  matrix = [[0 for i in range(4)] for j in range(2)]
  matrix[0][0]=row[1]
  matrix[0][1]=row[2]
  matrix[0][2]=row[6]
  matrix[0][3]=row[5]
  matrix[1][0]=row[0]
  matrix[1][1]=row[3]
  matrix[1][2]=row[7]
  matrix[1][3]=row[4]
  return matrix

def array2matrixPattern3(row):
  matrix = [[0 for i in range(4)] for j in range(2)]
  matrix[0][0]=row[0]
  matrix[0][1]=row[1]
  matrix[0][2]=row[5]
  matrix[0][3]=row[4]
  matrix[1][0]=row[3]
  matrix[1][1]=row[2]
  matrix[1][2]=row[6]
  matrix[1][3]=row[7]
  return matrix
  
def matrixmatch(matrixref,matrix2x4):
  match = True
  j=0
  while (j<2 and match):
    i=0
    while (i<4 and match):
      if matrix2x4[j][i]!=matrixref[j][i]:
        match= False
      i=i+1
    j=j+1
  return match
  
def matrix_circular_shift_left(matrix):
  new_matrix = [[0 for i in range(4)] for j in range(2)]
  new_matrix[0][0]=matrix[0][3]
  new_matrix[1][0]=matrix[1][3]
  for j in range (2):
    for i in range (0,3):
      new_matrix[j][i+1]=matrix[j][i]
  return new_matrix

# Compare matrix to matrixref if no match, shift ref matrix then compare try the shift 3 times to cover all possibilies. Return True if a match is found with the matrix or any of the 3 shifts else return false
def matrixMatchCircular(matrixref,matrix):
  new_matrix = [[0 for i in range(4)] for j in range(2)]
  new_matrix = matrixref
  counter = 0
  while not matrixmatch(new_matrix,matrix) and counter <= 3:
    new_matrix= matrix_circular_shift_left(new_matrix)  
    counter=counter+1
  if counter > 3:
    return False
  else:
    return True
    
def flipBaseWTop(matrix):
  new_matrix = [[0 for i in range(4)] for j in range(2)]
  j=0
  for i in range (0,4):
    new_matrix[j][i]=matrix[j+1][i]
    new_matrix[j+1][i]=matrix[j][i]
  return new_matrix

# Compare matrix with the Octaedre represented by Ref matrix, including shift 3 times and flip top with base then shift 3 times until a match is found or else return false no match
def matrixMatchRefMatrix(matrixref,matrix):
  match = False
  if not matrixMatchCircular(matrixref,matrix):
    flipped_matrix = flipBaseWTop(matrixref)
    match = matrixMatchCircular(flipped_matrix,matrix) 
  else:
    match = True
  return match

# Compare row with a reference row where we will try reference row pattern 1, 2 and 3
def compareRowto3RefPatternsMatrix(rowref,row):
  matrixref=array2matrix(rowref)
  matrix=array2matrix(row)
  # compare with first octaedre (including shift and flip top with base then shift)
  match = matrixMatchRefMatrix(matrixref,matrix)
  if not match:
    # Try to compare with pattern 2 
    matrixref=array2matrixPattern2(rowref)
    match = matrixMatchRefMatrix(matrixref,matrix)
    if not match:
      matrixref=array2matrixPattern3(rowref)
      match = matrixMatchRefMatrix(matrixref,matrix)
  return match
  
def compareRowtoList3RefPatternsMatrix(row,array_ref):
  array_size = len(array_ref)
  # print ("array size", array_size)
  found = False
  counter = 0
  while ((not found) and (counter < array_size)):
    if compareRowto3RefPatternsMatrix(array_ref[counter],row):
      # print("Found duplicate",counter)
      found = True
    else:
      counter+=1
  return found  
  
def removeDupRowfromList(array_in):
  res_array = [] # New array to build a table
  size_of_array_in = len(array_in)
  unique = 0
  duplicate = 0
  res_array.append(array_in[0])
  unique=unique+1
  for i in range (1, size_of_array_in):
    if not compareRowtoList3RefPatternsMatrix(array_in[i],res_array):
      # print ("non duplicate", array_in[i])
      res_array.append(array_in[i])
      unique=unique+1
      # print (valid_array[i], file=open("output.txt", "a"))
      # print (".", file=open("output.txt", "a")) # show loading
      # print (valid_array[i], file=open("output.txt", "a"))
    else:
      duplicate = duplicate + 1

  print("Total, Duplicate, Unique ",size_of_array_in,duplicate,unique)
  return res_array

def Method2Matrix(array_in):
  solution_array=removeDupRowfromList(array_in)
  # print results
  print ("\n Final result Method 2 ...",len(solution_array))
  counter=0
  for row in solution_array:
    counter=counter+1
    print("# ",counter,"    ", row)
  return
  print ("\n")

def Method1Row(c,n,twoDarr):
  # Put only valid rows with all colors in valid_array for further treatment
  # print("Cleaning arrays that doesn't contain all colors. Processing...")
  # valid_array = create_valid_arr(c,n,twoDarr)

  # print the outcome for verification
  # for row in valid_array:
  #  print(row)

  # Create new array non_dup_array that does not include any duplicate rows
  print("Removing duplicates...")
  #non_dup_array_stage1 = remove_duplicates(valid_array)
  non_dup_array_stage1 = remove_duplicates(twoDarr)

  # print the outcome for verification
  print ("Final result, or length of Non duplicates",len(non_dup_array_stage1))
  print ("Display final results:")
  for row in non_dup_array_stage1:
    print(row)
                   
  print ("Stage 1 Cleaning result...",len(non_dup_array_stage1), "\n")
  print("Calling the function to remove known duplicate stage 2...")
  final_array_clean_result = remove_duplicates_recursive(non_dup_array_stage1,0)
  print ("\n Final result Method 1 ...",len(final_array_clean_result))
  for row in final_array_clean_result:
    print(row)
    
  print ("\n")
  return
  
# main program
def m(c):
  print ("For", c, "colors...")
  # c = colors
  n = 8 #side - coté
  # total number of possibilities
  total_rows = c**n
  rows, cols = (total_rows,n)
  
  # define 2D array of c^n rows x n columns
  twoDarr = [[0 for i in range(cols)] for j in range(rows)]
  print("Calling the function to provide all possibilities. Processing...")
  # 2D array is the output of the function
  all_possibilities(c,n,twoDarr)

  # Method 1 with row comparison
  Method1Row(c,n,twoDarr)
  
  # Method 2 with Matrix structure 4x2
  Method2Matrix(twoDarr)

  # for troubleshooing purposes only
  #k=5
  #l=8
  #print ("Row[k]=",twoDarr[k])
  #print ("Row[l]=",twoDarr[l])
  
  #matrix=array2matrix(twoDarr[k])
  #matrixv3=array2matrix(twoDarr[l])
  #matrixv2=matrix_circular_shift_left(matrix)
  #matrixv2=matrix_circular_shift_left(matrixv2)
  #print ("matrix ..", matrix)
  #print ("matrix2x4v2 ..", matrixv2)
  
  #print ("CompareRowto3RefPatternsMatrix",CompareRowto3RefPatternsMatrix(twoDarr[k],twoDarr[l]))
  
  #print("match ..",matrixmatch(matrix,matrixv2))
  #print("match circular ..",matrixMatchCircular(matrix,matrixv3))
  #matrixv4 = flipBaseWTop(matrix)
  #matrixv5 = flipBaseWTop(matrixv3)
  #print("flipBaseWTop..", matrixv4)
  #print("array..",twoDarr[91])
  #print("matrixMatchRefMatrix",matrixMatchRefMatrix(matrix,matrixv5))
  #print("array2matrixPattern3..", array2matrixPattern3(twoDarr[91]))
  #print("array2matrixPattern3..", array2matrixPattern3(twoDarr[250]))
