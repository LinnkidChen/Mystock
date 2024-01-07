import { createApp } from "vue";
import ElementPlus from 'element-plus'
import { createPinia } from "pinia";
// import "element-plus/dist/index.css";
import App from "./App.vue";
import router from "./router"
import "@/styles/index.scss";
// import "./styles/index.scss";

// import ElementPlus from "element-plus";
// import all element css, uncommented next line


// or use cdn, uncomment cdn link in `index.html`

// If you want to use ElMessage, import it.

// import "element-plus/theme-chalk/src/message.scss";

const app = createApp(App);
app.use(createPinia)
app.use(ElementPlus);
app.use(router)
app.mount("#app");
