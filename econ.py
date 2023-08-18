from UtilsDirectory.data import *

def get_user_inventory(user_id):
    # Get the user's inventory, or create a new one if it doesn't exist
    inventory_file = f"inventory/{user_id}.json"
    if os.path.exists(inventory_file):
        with open(inventory_file, "r") as f:
            user_inventory = json.load(f)
    else:
        user_inventory = {
                            "gold": 10000,
                            "items": [
                                
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

    with open(f"inventory/{user_id}.json", "w") as f:
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
    async def view(self, ctx, choice, optional):
        """Shows the user's inventory"""
        
        if choice == "inventory":
            if optional == "me":
                inventory = get_user_inventory(ctx.author.id)
            else:
                inventory = get_user_inventory(str(optional))

            # Send a message listing all the items in the inventory
            if not inventory:
                await ctx.send("Your inventory is empty.")
            else:
                gold = inventory["gold"]
                items = inventory["items"]

                items_str = "\n".join(f"- {item['name']} (x{item['quantity']})" for item in items)

                message = f"```Here is your inventory:\n\nGold: {gold}\n\nItems:\n{items_str}```"
                await ctx.send(message)
        elif choice == "lootbox":
            lootbox_file = f"lootbox/{optional}.json"
            if not os.path.exists(lootbox_file):
                await ctx.send(f"{optional} is not a valid lootbox.")
                return

            with open(lootbox_file, "r") as f:
                lootbox_data = json.load(f)
                f.close()

            items = lootbox_data['items']
            cost = lootbox_data['cost']

            items_str = "\n".join(f"- {item['item_name']} (x{item['quantity']})" for item in items)

            message = f"```Here is the {lootbox_data['name']}\n\nCost: {cost}\n\nItems:\n{items_str}```\n"
            await ctx.send(message)


#await ctx.send('Check!')

    
    @commands.command()
    async def lootbox(self, ctx, lootbox_name: str):
        """Opens a lootbox and rewards the user with a random item"""
        # Load the lootbox data from a JSON file

        player_inv = get_user_inventory(ctx.author.id)
        lootbox_file = f"lootbox/{lootbox_name}.json"
        if not os.path.exists(lootbox_file):
            await ctx.send(f"{lootbox_name} is not a valid lootbox.")
            return

        with open(lootbox_file, "r") as f:
            lootbox_data = json.load(f)
            f.close()

        if player_inv['gold'] < lootbox_data['cost']:
            await ctx.send(f"You ain't got the gold for that bub. Sorry man.")
            return
        else:
            add_gold_to_inventory(ctx.author.id, (int(lootbox_data['cost']) * -1))

        # Choose a random item from the lootbox and reward the user
        loot = random.choices(lootbox_data["items"],lootbox_data["weights"])
        loot = loot[0]
        
        item_name = loot["item_name"]
        item_type = loot["item_type"]
        item_quantity = loot["quantity"]

        await ctx.send(f"You got {item_quantity} {item_name}(s) from the {lootbox_name} lootbox!")

        if item_name == "Gold Coin":
            add_gold_to_inventory(ctx.author.id,int(item_quantity))
        else:
            add_item_to_inventory(ctx.author.id, item_name, item_type, item_quantity)

    @commands.command()
    async def sell(self, ctx, item, amount: int):
        """Sells the desired item"""
        inventory = get_user_inventory(ctx.author.id)
        with open(f"inventory/prices.json", "r") as f:
            price_chart = json.load(f)
            f.close()

        # Send a message listing all the items in the inventory
        if not inventory["items"]:
            await ctx.send("Your inventory is empty.")
        else:
            gold = inventory["gold"]
            items = inventory["items"]

            if not items[f'{item}']:
                await ctx.send(f"You don't have any {item} in your inventory")
            
            await ctx.send(f"{items}")


async def setup(client):
    await client.add_cog(Econ(client))