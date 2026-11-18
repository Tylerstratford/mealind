import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import MealPlanner from './views/MealPlanner.vue'
import ShoppingList from './views/ShoppingList.vue'
import Recipes from './views/Recipes.vue'
import MyRecipes from './views/MyRecipes.vue'
import AddRecipe from './views/AddRecipe.vue'
import DesignMock from './views/DesignMock.vue'
import DesignMock2 from './views/DesignMock2.vue'
import DesignMock3 from './views/DesignMock3.vue'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/planner' },
    { path: '/planner', component: MealPlanner },
    { path: '/shopping', component: ShoppingList },
    { path: '/recipes', component: Recipes },
    { path: '/my-recipes', component: MyRecipes },
    { path: '/add-recipe', component: AddRecipe },
    { path: '/edit-recipe/:id', component: AddRecipe },
    { path: '/design-mock', component: DesignMock },
    { path: '/design-mock-2', component: DesignMock2 },
    { path: '/design-mock-3', component: DesignMock3 }
  ]
})

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')
