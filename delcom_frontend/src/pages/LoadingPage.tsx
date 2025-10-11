import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function LoadingPage() {
  const [progress, setProgress] = useState(0);

  const [dots, setDots] = useState("");

  const navigate = useNavigate();

  const [displayText, setDisplayText] = useState("");
  const [factIndex, setFactIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  const funFacts = [
    "If you have any feedback or suggestions, feel free to email williamhnyman@gmail.com!",
    "Apples float in water because they are 25% air!",
    "Carrots were originally purple, not orange!",
    "Bananas are technically berries!",
    "Strawberries are not true berries!",
    "Honey never spoils!",
    "Pineapples take about two years to grow!",
    "Tomatoes were once considered poisonous in Europe!",
    "Ketchup was once sold as medicine!",
    "Broccoli contains more protein per calorie than steak!",
    "Peanuts are not nuts—they’re legumes!",
    "Coffee beans are actually seeds from a fruit!",
    "Chocolate was once used as currency by the Aztecs!",
    "Lettuce is a member of the sunflower family!",
    "Celery has negative calories because digesting it burns more energy than it provides!",
    "Cucumbers are 96% water!",
    "Potatoes were the first vegetable grown in space!",
    "Almonds are seeds, not nuts!",
    "Popcorn is the oldest snack in the world, dating back thousands of years!",
    "Arachibutyrophobia is the fear of peanut butter sticking to the roof of your mouth!",
    "Applesauce was the first food eaten in space!",
    "Cabbage has more vitamin C than oranges!",
    "The average ear of corn has 16 rows of kernels!",
    "Cashews grow on the bottom of a fruit called the cashew apple!",
    "An egg’s shell color doesn’t affect its taste or nutrition!",
    "Chewing gum was banned in Singapore until 2004!",
    "The most expensive pizza in the world costs over $10,000!",
    "Mangoes are the most consumed fruit in the world!",
    "White chocolate isn’t technically chocolate because it has no cocoa solids!",
    "Wasabi is often just colored horseradish!",
    "Watermelons are both a fruit and a vegetable!",
    "There are more than 7,500 varieties of apples grown worldwide!",
    "One spaghetti noodle is called a spaghetto!",
    "French fries actually originated in Belgium, not France!",
    "Chili peppers trick your brain into thinking your mouth is burning!",
    "Grapes explode if you microwave them!",
    "The popsicle was invented by accident by an 11-year-old!",
    "Cotton candy was invented by a dentist!",
    "Peppers have more vitamin C than oranges!",
    "Egg yolks are one of the few foods that naturally contain vitamin D!",
    "Avocados ripen faster when stored with bananas!",
    "Fortune cookies were invented in California, not China!",
    "Soy sauce can take up to two years to make!",
    "Oranges are a hybrid of pomelo and mandarin!",
    "Cherries are related to roses!",
    "Ice cream cones were popularized at the 1904 World’s Fair in St. Louis!",
    "Each pineapple plant produces only one pineapple at a time!",
    "Some cheeses are aged in caves!",
    "The most expensive spice in the world is saffron!",
    "Cauliflower comes in purple, orange, and green varieties!",
    "Oysters can change their gender multiple times in their life!",
    "Cranberries bounce when they are ripe!",
    "Coconut water can be used as an emergency blood substitute!",
    "Peppers are measured for spiciness using Scoville Heat Units!",
    "The mushroom is more closely related to animals than plants!",
    "Nutmeg is toxic in large doses!",
    "Caramel was first made in the 17th century!",
    "Rice is the staple food for over half the world’s population!",
    "The sandwich was named after the Earl of Sandwich!",
    "Cheese is the most stolen food in the world!",
    "Pizza is the most popular food in the world!",
    "The largest pumpkin ever grown weighed over 2,700 pounds!",
    "The world’s most expensive coffee is made from beans eaten and excreted by a civet!",
    "Popcorn was eaten by Native Americans over 5,000 years ago!",
    "Alaska is the only state in the U.S. that grows coffee commercially!",
    "Lobsters used to be considered poor man’s food!",
    "Sushi does not mean raw fish—it means vinegared rice!",
    "Olives can’t be eaten right off the tree—they’re too bitter!",
    "Blueberries are one of the only naturally blue foods!",
    "Kiwis were originally called Chinese gooseberries!",
    "There are more than 600 pasta shapes worldwide!",
    "Maple syrup is made from the sap of maple trees!",
    "Vanilla is the second most expensive spice after saffron!",
    "Apples are part of the rose family!",
    "Bell peppers can be green, red, yellow, orange, or even purple!",
    "Peaches are related to almonds!",
    "Swiss cheese has holes due to bacteria releasing carbon dioxide during fermentation!",
    "The most expensive cheese is made from donkey milk!",
    "The Guinness World Record for the largest chocolate bar weighed over 12,000 pounds!",
    "A cluster of bananas is called a hand, and a single banana is called a finger!",
    "Carrots are rich in beta-carotene, which helps maintain good vision!",
    "Spinach was Popeye’s source of strength because of its iron content!",
    "The jalapeño is named after the Mexican city of Xalapa!",
    "Quinoa is a seed, not a grain!",
    "Chickpeas are also known as garbanzo beans!",
    "Orzo pasta looks like rice but is made from wheat!",
    "Caviar is made from sturgeon fish eggs!",
    "The popsicle was patented in 1924!",
    "Cinnamon comes from the inner bark of a tree!",
    "Apricots are closely related to plums and cherries!",
    "The average person eats about 35 tons of food in their lifetime!",
    "Cantaloupes are named after Cantalupo, Italy, where they were first cultivated in Europe!",
    "Peppers originated in Central and South America!",
    "Brussels sprouts are named after Brussels, Belgium!",
    "Eggplants are technically berries!",
    "A tomato is both a fruit and a vegetable depending on context!",
    "Pomegranates can have over 1,000 seeds inside!",
    "Sweet potatoes are not related to regular potatoes!",
    "Radishes were one of the first vegetables cultivated by humans!",
    "Garlic was used as medicine in ancient Egypt!",
    "Mint was once used as currency in ancient Greece!",
    "The Caesar salad was invented in Mexico, not Italy!",
    "The word “salad” comes from the Latin word for salt!",
    "Yogurt has been eaten for over 4,500 years!",
  ];

  // Progress polling
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("https://delcom.onrender.com/progress");
        const data = await res.json();
        setProgress(data.value);

        if (data.done) {
          clearInterval(interval);

          // fetch final result
          const resultRes = await fetch("https://delcom.onrender.com/result");
          const resultData = await resultRes.json();

          // navigate to results page with data
          setTimeout(() => {
            navigate("/results", { state: { result: resultData } });
          }, 2500); // slight delay to show 100% progress bar
        }
      } catch (err) {
        console.error("Error polling progress:", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [navigate]);

  // Dots animation
  useEffect(() => {
    const dotInterval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 500);

    return () => clearInterval(dotInterval);
  }, []);

  // fun fact animation
  useEffect(() => {
    const currentFact = funFacts[factIndex];

    let timer: ReturnType<typeof setTimeout>;

    if (!isDeleting && displayText.length < currentFact.length) {
      // typing forward
      timer = setTimeout(() => {
        setDisplayText(currentFact.slice(0, displayText.length + 1));
      }, 100);
    } else if (isDeleting && displayText.length > 0) {
      // deleting
      timer = setTimeout(() => {
        setDisplayText(currentFact.slice(0, displayText.length - 1));
      }, 50);
    } else if (!isDeleting && displayText.length === currentFact.length) {
      // pause before deleting
      timer = setTimeout(() => setIsDeleting(true), 1500);
    } else if (isDeleting && displayText.length === 0) {
      // move to next fact
      setIsDeleting(false);
      setFactIndex(() => Math.floor(Math.random() * funFacts.length));
    }

    return () => clearTimeout(timer);
  }, [displayText, isDeleting, factIndex]);

  return (
    <div className="main-content">
      <h1
        className="title"
        style={{
          fontFamily: "Poppins",
          display: "flex",
          justifyContent: "center", // centers the whole thing
          alignItems: "center",
          gap: "2px", // small space between text and dots
          marginLeft: "21px",
        }}
      >
        <span>Loading results</span>
        <span style={{ minWidth: "1.5em", textAlign: "left" }}>{dots}</span>
      </h1>

      <div
        style={{
          width: "60%",
          background: "white",
          borderRadius: "7px",
          border: "2px solid #ffffffff", // sky blue border
          marginTop: "1rem",
        }}
      >
        <div
          style={{
            width: `${progress}%`,
            background: "#F4A261", // coral fill
            height: "20px",
            borderRadius: "5px",
            transition: "width 0.5s ease",
          }}
        />
      </div>

      <p className="funfact">
        {displayText}
        <span className="blinking-cursor">|</span>
      </p>

      {/*<p>{progress}%</p>*/}
    </div>
  );
}

export default LoadingPage;
