import { autoinject, observable, TaskQueue, Aurelia } from 'aurelia-framework';
import { Router, RouteConfig, RouterConfiguration } from 'aurelia-router'
import { PLATFORM } from 'aurelia-pal';
import { DefaultApi } from './gen-openapi';
// import { HttpClient } from 'aurelia-fetch-client';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';
// import { Luncho, LunchoResult} from './luncho';

@autoinject
export class App {
    public title: string = 'Luncho';
    public router: Router;
    public static app: App;
    show = false;
    countries: any;
    // luncho: Luncho;
    public taskQueue: TaskQueue;
    public api: DefaultApi;


    constructor(taskQueue: TaskQueue, router: Router, api: DefaultApi) {
        this.taskQueue = taskQueue;
        this.api = api;
        this.api.basePath = 'http://localhost:8000'
        // this.luncho = new Luncho(taskQueue);
        App.app = this;
        this.router = router;
    }

    activate() {
        this.api.countries()
            .then((countries) => {
                this.countries = countries;
        });
    }

    // attached() {
    //     this.countryCode = 'JPN';
    //     //super.attached();
    // }


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
