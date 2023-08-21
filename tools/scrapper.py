import requests
import pickle
from bs4 import BeautifulSoup
from datetime import datetime

def getSoup(url='none'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

data = []
max_page = 0
fetch_errors = 0

print('\033[93mFetching Courses...')
  
refetch_status = False
soup = getSoup(url='https://www.coursera.org/courses?query=python&page=1&index=prod_all_launched_products_term_optimization')
pageNumberNavigationBar = soup.find_all("a", class_="cds-119 cds-113 cds-115 box number css-4n7kh3 cds-142")
for pageNumber in pageNumberNavigationBar:
  max_page = int(pageNumber.text)

for page in range(1, max_page, 1):

  print(F'Working on Page {page} / {max_page} | Found {len(data)}', end="\r")
  soup = getSoup(url=f'https://www.coursera.org/courses?query=python&page={str(page)}&index=prod_all_launched_products_term_optimization')
  results = soup.find_all("li", class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76")
  
  
  for course in results:
    try:
      author_element = course.find("span", class_="cds-119 css-1mru19s cds-121")
      course_title = course.find("h2", class_="cds-119 css-h1jogs cds-121")
      skills_gained = course.find("p", class_="cds-119 css-12ksubz cds-121")
      course_rating = course.find("p", class_="cds-119 css-11uuo4b cds-121")
      review_count = course.find("p", class_="cds-119 css-dmxkm1 cds-121")
      course_duration = course.find("p", class_="cds-119 css-dmxkm1 cds-121")
      course_link = course.find("a")

      if ('learn' in course_link["href"]):
        data.append([author_element.text, course_title.text, skills_gained.text, course_rating.text, review_count.text, f'https://www.coursera.org{course_link["href"]}', []])
      
    except:
      fetch_errors += 1
      break
print(f'\033[92m\nFetched total {len(data)} courses with {fetch_errors} fetch errors!')
  
print('\033[93mInitiating Module Data Extratction...')
retryModule = True
for courseNum, course in enumerate(data):
  print(f'Working on Module {courseNum+1} / {len(data)}', end="\r")
  while retryModule == True:
    try:
      module_info = []
      VRQ_Info = '' #VRQ = Video, Reading, Quiz
      soup = getSoup(url=course[5])
      rootModule = soup.find("div", class_="cds-AccordionRoot-container cds-AccordionRoot-silent")
      module_number_time = rootModule.find("div", class_="cds-119 css-mc13jp cds-121")
      module_number, module_time = module_number_time.text.split("•", 1)
      module_title = rootModule.find("h3", class_="cds-119 css-h1jogs cds-121")
      module_description = rootModule.find("p", class_="cds-119 css-80vnnb cds-121")
      module_included = rootModule.find_all("h5", class_="cds-119 css-1wrljd2 cds-121")
      if len(module_included) !=0:
        for VRQ_Raw_Info in module_included:
          VRQ_Info += f' | {VRQ_Raw_Info.text}'
    
      module_info.append([module_number, module_title.text, module_description.text, module_time, VRQ_Info])
    
      childModules = soup.find_all("div", class_="cds-AccordionGroup-itemSpacing")
      for module in childModules:
        try:
          VRQ_Info = ''
          module_number_time = module.find("div", class_="cds-119 css-mc13jp cds-121")
          module_number, module_time = module_number_time.text.split("•", 1)
          module_title = module.find("h3", class_="cds-119 css-h1jogs cds-121")
          module_description = module.find("p", class_="cds-119 css-80vnnb cds-121")
          module_included = module.find_all("h5", class_="cds-119 css-1wrljd2 cds-121")
          if len(module_included) !=0:
            for VRQ_Raw_Info in module_included:
              VRQ_Info += f' | {VRQ_Raw_Info.text}'
        
          module_info.append([module_number, module_title.text, module_description.text, module_time, VRQ_Info])
        except:
          pass
        retryModule = False
    except:
      retryModule = True
    

  course[6] = module_info

input(f'\nShowing {len(data)} results. | Enter to Display')
print('Jeez, do you want to kill the terminal? Lemme store it for you in a pickle jar!')
with open(f'{len(data)}_UltraExpensive_VeryDeep_DataSet_{datetime.now()}.pkl', 'wb') as file:
    pickle.dump(data, file)
print('Okay, all done, enjoy the tasty data! :)')
