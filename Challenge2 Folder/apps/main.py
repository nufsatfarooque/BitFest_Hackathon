from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import Ingredient, Recipe, engine, Base, sessionmaker
import re
import openai

app = FastAPI()


#database session
SessionLocal = sessionmaker(bind=engine)
router = APIRouter()
app.include_router(router)


#db session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"msg": "Welcome to Mofa's Recipe Manager!"}

@app.post("/ingredients")
def add_or_update_ingredients(name: str, quantity: float, db: Session = Depends(get_db)):
    #check if exist
    ingredient = db.query(Ingredient).filter(Ingredient.name == name).first()

    if ingredient:
        ingredient.quantity+=quantity
        db.commit()
        return{"msg": f"Ingredient '{name}' updated successfully"}
    else:
        ingredient = Ingredient(name=name, quantity=quantity)
        db.add(ingredient)
        db.commit()
        return{"msg": f"Ingredient '{name}' added successfully"}
    

@app.post("/recipe")
def import_recipes(db: Session = Depends(get_db)):
    try:
        with open("my_fav_recipes.txt", "r") as file:
            lines = file.readlines()

        # Ensure lines are properly structured
        for i in range(0, len(lines), 6):
            try:
                if i + 5 >= len(lines):  # Prevent out-of-range errors
                    raise ValueError("Incomplete recipe entry found at the end of the file.")

                name_line = lines[i].strip()
                ingredients_line = lines[i+1].strip()
                taste_line = lines[i+2].strip()
                cuisine_line = lines[i+3].strip()
                prep_time_line = lines[i+4].strip()
                instructions_line = lines[i+5].strip()

                print(name_line)

                # Extract fields and validate
                if not (name_line.startswith("Name:") and 
                        ingredients_line.startswith("Ingredients:") and 
                        taste_line.startswith("Taste:") and 
                        cuisine_line.startswith("Cuisine Type:") and 
                        prep_time_line.startswith("Preparation Time:") and 
                        instructions_line.startswith("Instructions:")):
                    raise ValueError(f"Malformed recipe entry at line {i+1}")

                # Create Recipe object
                recipe = Recipe(
                    name=name_line.split(": ", 1)[1].strip(),
                    ingredients=ingredients_line.split(": ", 1)[1].strip(),
                    taste=taste_line.split(": ", 1)[1].strip(),
                    cuisine_type=cuisine_line.split(": ", 1)[1].strip(),
                    preparation_time=int(prep_time_line.split(": ", 1)[1].split()[0]),
                    instructions=instructions_line.split(": ", 1)[1].strip()
                )
                db.add(recipe)
            except Exception as e:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Error parsing recipe at line {i+1}: {str(e)}"
                )

        db.commit()
        return {"message": "Recipes imported successfully!"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/recipes/raw")
def add_recipe_raw(text: str):
    try:
        # Try to extract key details using simple regex patterns or string operations
        name_match = re.search(r"(?<=Name:)(.*?)(?=\n|$)", text)
        ingredients_match = re.search(r"(?<=Ingredients:)(.*?)(?=\n|$)", text)
        taste_match = re.search(r"(?<=Taste:)(.*?)(?=\n|$)", text)
        cuisine_match = re.search(r"(?<=Cuisine:)(.*?)(?=\n|$)", text)
        prep_time_match = re.search(r"(?<=Preparation Time:)(.*?)(?=\n|$)", text)
        instructions_match = re.search(r"(?<=Instructions:)(.*?)(?=\n|$)", text)

        if not all([name_match, ingredients_match, taste_match, cuisine_match, prep_time_match, instructions_match]):
            raise HTTPException(status_code=400, detail="Could not extract all necessary fields")

        # If matches are found, save to the file
        with open("my_fav_recipes.txt", "a") as file:
            file.write(f"Name: {name_match.group(1).strip()}\n")
            file.write(f"Ingredients: {ingredients_match.group(1).strip()}\n")
            file.write(f"Taste: {taste_match.group(1).strip()}\n")
            file.write(f"Cuisine: {cuisine_match.group(1).strip()}\n")
            file.write(f"Preparation Time: {prep_time_match.group(1).strip()}\n")
            file.write(f"Instructions: {instructions_match.group(1).strip()}\n\n")

        return {"message": "Recipe added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing the recipe: {str(e)}")
   

openai.api_key = "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"


@app.post("/chat")
def chat_with_user(user_input: str, db: Session = Depends(get_db)):
    """
    Process user input, query recipes and ingredients, and recommend recipes.
    """
    #  Use the LLM to extract preferences
    messages = [
        {"role": "system", "content": "You are a helpful assistant that understands food preferences."},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        max_tokens=50
    )

    
    preference_analysis = response["choices"][0]["message"]["content"]
    keywords = extract_keywords(preference_analysis)  #

    # search the recipes table
    matching_recipes = db.query(Recipe).filter(
        Recipe.ingredients.any(Ingredient.name.in_(keywords))
    ).all()

    # Check ingredient availability
    available_recipes = []
    for recipe in matching_recipes:
        required_ingredients = {ingredient.name for ingredient in recipe.ingredients}
        available_ingredients = {i.name for i in db.query(Ingredient).filter(Ingredient.available == True).all()}
        
        if required_ingredients.issubset(available_ingredients):
            available_recipes.append(recipe.name)

    # Recommend recipes
    if available_recipes:
        return {"recommendations": available_recipes}
    else:
        return {"message": "No recipes match your preferences with the available ingredients."}

def extract_keywords(preference_analysis: str):
    """
    Extract relevant keywords from the LLM response.
    Example: Input "I want something sweet" -> Output ["sweet", "sugar"]
    """
    # Simple keyword mapping 
    keyword_map = {
        "sweet": [
            "sugar", "honey", "chocolate", "jam"
        ],
        "spicy": [
            "chili", "pepper", "black pepper"
        ],
        "savory": [
            "salt", "soy sauce", "garlic", "onion"
        ],
        "sour": [
            "lemon", "lime", "vinegar", "pickle", "tamarind"
        ],
        "bitter": [
            "dark chocolate", "coffee", "cocoa"
        ],
        "fruit": [
            "apple", "banana", "berry", "orange"
        ]
    }

    extracted_keywords = []
    for key, values in keyword_map.items():
        if key in preference_analysis.lower():
            extracted_keywords.extend(values)

    return extracted_keywords

