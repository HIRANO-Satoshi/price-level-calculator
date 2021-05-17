import { autoinject, TaskQueue } from 'aurelia-framework';
import { Router, RouterConfiguration } from 'aurelia-router'
import { PLATFORM } from 'aurelia-pal';
import { Luncho } from 'luncho-typescript-aurelia/luncho';

@autoinject
export class App {
    public title: string = 'Luncho';
    public router: Router;
    public static app: App;
    show = false;
    public taskQueue: TaskQueue;
    luncho: Luncho;


    constructor(taskQueue: TaskQueue, router: Router, luncho: Luncho) {
        this.taskQueue = taskQueue;
        this.luncho = luncho;
        this.luncho.basePath = 'http://localhost:8000'
        App.app = this;
        this.router = router;
    }

    toggleSideNav() {
        this.show = !this.show;
    }

    configureRouter(config: RouterConfiguration, router: Router) {
        this.router = router;
        config.title = this.title;

        //config.addPipelineStep('authorize', AuthorizeStep); // add login
        config.map([
            { route: ['', 'single'], href: '/single', name: '#/single',
              moduleId: PLATFORM.moduleName('./single'),
              auth: true, nav: true, title: 'One country', },
            { route: 'countries', href: '/countries', name: '#/countries',
              moduleId: PLATFORM.moduleName('./countries'),
              auth: true, nav: true, title: 'All countries', },
            { route: 'about', href: 'about', name: 'about',
              moduleId: PLATFORM.moduleName('./about'),
              auth: true, nav: false, title: 'About', },

        ]);

        config.fallbackRoute('/');
    }
}
