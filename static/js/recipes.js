const deleteRecipeModal = new bootstrap.Modal(document.getElementById("deleteRecipeModal"));
const deleteRecipeButton = document.getElementsByClassName("delete-recipe");
const deleteRecipeConfirm = document.getElementById("deleteRecipeConfirm");



/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/

for (let button of deleteRecipeButton) {
    button.addEventListener("click", (e) => {
      let recipeId = e.target.getAttribute("recipe_id");
      deleteRecipeConfirm.href = `delete_submitted_recipe/${recipeId}`;
      deleteRecipeModal.show();
    });
  }