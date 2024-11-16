from flask import Flask, request, jsonify  # Import Flask framework and tools for handling requests and responses
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import random  # Import random module for random operations

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Function to calculate the fitness of a route
def calculate_fitness(route, points):
    """
    Calculate the total distance of the route.
    The shorter the distance, the higher the fitness.
    :param route: List of indices representing the order of points in the route
    :param points: List of (x, y) coordinates of points
    :return: Total distance of the route
    """
    return sum(
        ((points[route[i]][0] - points[route[i+1]][0])**2 + 
         (points[route[i]][1] - points[route[i+1]][1])**2)**0.5
        for i in range(len(route)-1)
    )

# Function implementing the Genetic Algorithm to find the optimal path
def genetic_algorithm(points):
    """
    Find the shortest route connecting all points using a Genetic Algorithm.
    :param points: List of (x, y) coordinates of points
    :return: Optimal route as a list of points
    """
    population_size = 50  # Number of routes in the population
    generations = 500  # Number of iterations to evolve
    mutation_rate = 0.1  # Probability of mutation

    # Generate initial random population (list of random routes)
    population = [random.sample(range(len(points)), len(points)) for _ in range(population_size)]

    # Evolve the population over multiple generations
    for _ in range(generations):
        # Calculate fitness for each route and sort the population by fitness (ascending order)
        population = sorted(population, key=lambda route: calculate_fitness(route, points))

        # Keep only the top half of the population (selection step)
        population = population[:population_size // 2]

        # Generate a new population through crossover and mutation
        new_population = []
        while len(new_population) < population_size:
            # Select two parents randomly from the top half of the population
            parent1, parent2 = random.sample(population, 2)
            
            # Perform crossover: create a child by combining segments of both parents
            cut = len(parent1) // 2
            child = parent1[:cut] + [gene for gene in parent2 if gene not in parent1[:cut]]

            # Perform mutation with a given probability
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(child)), 2)  # Select two random indices
                child[i], child[j] = child[j], child[i]  # Swap two cities

            new_population.append(child)  # Add the new child to the new population
        
        # Update the population for the next generation
        population = new_population

    # Select the best route from the final population
    optimal_route = min(population, key=lambda route: calculate_fitness(route, points))
    
    # Convert the route indices back to coordinates
    return [points[i] for i in optimal_route]

# Route for the home page
@app.route('/')
def home():
    """
    Home route for the API.
    :return: A welcome message
    """
    return "Welcome to the Truck Route Optimization API!"

# Route to optimize the route
@app.route('/optimize-route', methods=['POST'])
def optimize_route():
    """
    API endpoint to find the optimal route for a given set of points.
    :return: JSON response with the optimal route or error message
    """
    try:
        data = request.get_json()  # Parse JSON request
        points = data['points']  # Extract points from the request
        
        # Validate the input points
        if not points or len(points) < 2:
            return jsonify({'error': 'Please provide at least two points'}), 400

        # Find the optimal route using the genetic algorithm
        optimal_route = genetic_algorithm(points)
        print("Optimal route:", optimal_route)  # Log the result for debugging
        return jsonify({'optimalRoute': optimal_route})  # Return the result as JSON
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': 'An error occurred on the server.'}), 500

# Main entry point to run the Flask app
if __name__ == '__main__':
    app.run(port=3000)  # Run the application on port 3000
