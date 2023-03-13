from UtilsDirectory.data import *

def get_user_inventory(user_id):
    # Get the user's inventory, or create a new one if it doesn't exist
    inventory_file = f"inventory/{user_id}.json"
    if os.path.exists(inventory_file):
        with open(inventory_file, "r") as f:
            user_inventory = json.load(f)
    else:
        user_inventory = {
                            "gold": 100,
                            "items": [
                                
                             ],
                            "lootboxes": [
                                
                            ]
                        }
        with open(f"inventory/{user_id}.json", "w") as f:
            json.dump(user_inventory, f)

    return user_inventory

def add_item_to_inventory(user_id, item_name: str, item_type: str,  quantity: int):
    inventory = get_user_inventory(user_id)

    items = inventory["items"]
    for item in items:
        if item["name"] == item_name:
            item["quantity"] += quantity
            break
    else:
        items.append({"name": item_name, "type": item_type, "quantity": quantity})

    with open("inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

def add_gold_to_inventory(user_id, amount: int):
    inventory = get_user_inventory(user_id)

    inventory["gold"] += amount

    with open(f"inventory/{user_id}.json", "w") as f:
        json.dump(inventory, f, indent=4)

class Econ(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Create the inventory directory if it doesn't exist
        if not os.path.exists("inventory"):
            os.makedirs("inventory")
        
        if not os.path.exists("lootbox"):
            os.makedirs("lootbox")

    @commands.command()
    async def viewinventory(self, ctx):
        """Shows the user's inventory"""
        inventory = get_user_inventory(ctx.author.id)

        # Send a message listing all the items in the inventory
        if not inventory:
            await ctx.send("Your inventory is empty.")
        else:
            gold = inventory["gold"]
            items = inventory["items"]
            lootboxes = inventory["lootboxes"]

            items_str = "\n".join(f"- {item['name']} (x{item['quantity']})" for item in items)
            lootboxes_str = "\n".join(f"- {box['name']} (x{box['count']})" for box in lootboxes)

            message = f"```Here is your inventory:\n\nGold: {gold}\n\nItems:\n{items_str}\n\nLootboxes:\n{lootboxes_str}```"
            await ctx.send(message)

    
    @commands.command()
    async def olb(self, ctx, lootbox_name: str):
        """Opens a lootbox and rewards the user with a random item"""
        # Load the lootbox data from a JSON file
        lootbox_file = f"lootbox/{lootbox_name}.json"
        if not os.path.exists(lootbox_file):
            await ctx.send(f"{lootbox_name} is not a valid lootbox.")
            return

        with open(lootbox_file, "r") as f:
            lootbox_data = json.load(f)

        # Choose a random item from the lootbox and reward the user
        loot = random.choice(lootbox_data["items"])
        item_name = loot["item_name"]
        item_type = loot["item_type"]
        item_quantity = loot["quantity"]
        await ctx.send(f"You got {item_quantity} {item_name}(s) from the {lootbox_name} lootbox!")
        
        add_item_to_inventory(ctx.author.id, item_name, item_type, item_quantity)

    @commands.command()
    async def createlootbox(self, ctx, lootbox_name: str, *, lootbox_data: str):
        """Creates a new lootbox with the given name and data"""
        # Parse the lootbox data as JSON
        try:
            lootbox_items = json.loads(lootbox_data)
        except json.JSONDecodeError:
            await ctx.send("Invalid lootbox data format. Please provide a valid JSON object.")
            return

        # Save the lootbox data to a JSON file
        lootbox_file = f"lootbox/{lootbox_name}.json"
        with open(lootbox_file, "w") as f:
            json.dump(lootbox_items, f)

        await ctx.send(f"Created lootbox {lootbox_name} with data: {lootbox_data}")

    @commands.command()
    async def deletelootbox(self, ctx, lootbox_name: str):
        """Deletes a lootbox with the given name"""
        # Delete the lootbox file
        lootbox_file = f"lootbox/{lootbox_name}.json"
        if os.path.exists(lootbox_file):
            os.remove(lootbox_file)
            await ctx.send(f"Deleted lootbox {lootbox_name}")
        else:
            await ctx.send(f"{lootbox_name} is not a valid lootbox.")

async def setup(client):
    await client.add_cog(Econ(client))