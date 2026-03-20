import {record} from "#nuxt-scripts/validation/mock";
import Toucher from "../../../libs/jsa-client/jsalchemy/ts/Toucher";
import type {IOrmOptions, IResource} from "../../../libs/jsa-client/jsalchemy/ts/interfaces";
import Orm from "../../../libs/jsa-client/jsalchemy/ts/Orm";
import Collection from "../../../libs/jsa-client/jsalchemy/ts/Collection";
import RSet from "../../../libs/jsa-client/jsalchemy/ts/RSet";
import _ from 'lodash';

export interface ITest {
    func: Function,
    id: string,
    status: string,
    error?: string,
}

function sleep(ms: number): Promise<null> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function arrayEqual(a1: string[], a2: string[]): boolean {
    if (a1.length !== a2.length)
        return false
    for (let i = 0; i < a1.length; i ++) {
        if (a1[i] !== a2[i])
            return false;
    }
    return true
}

function objectEqual(o1: Object, o2: Object): boolean {
    let keys = Object.keys(o1);
    if (Object.keys(o2).length !== keys.length)
        return false
    for (let key of keys) {
        if (o1[key] !== o2[key])
            return false
    }
    return true
}

function range(_from: number = 0, to: number = 0) {
    if (to === 0) {
        to = _from
        _from = 0;
    }
    return Array.from({length: to - _from}, (_, i) => _from + i)
}

const ormOptions: IOrmOptions = {
  endpoint: '/jsalchemy',
  autologin: true,
  keepSession: 3600,
  // ws: {
  //   host: 'localhost',
  //   port: 7998,
  //   channel: 'js-router'
  // }
}

window.ormOptions = ormOptions;

class TestInstance implements IResource {
    $pk: string
    $row: Object
    $raw: Object
    $dirty: boolean
    $attributeTypes: Object
    // $collection: Collection
    [key: string]: any

    constructor(ob: object | any) {
        this.$row = ob;
        this.$raw = ob;
        this.$dirty = false
        this.name = ob.name || 'No Name';
        this.$pk = ob.$pk || '';
        this.score = ob.score || 0.1;
        this.$attributeTypes = [];
    }
}

const fixtures = {
    async alones(numItems: number = 300): Promise<Orm> {
        let orm = new Orm(ormOptions);
        const Alone = await orm.getModel('Alone');
        await Alone.deleteAll();
        const alones = [];
        for (let i = 0; i < numItems; i ++) {
            alones.push(new Alone({name: `Alone ${i % 10}`, score: i * 0.5, date: new Date()}));
        }
        await orm.saveBulk(alones);
        return window.orm = new Orm(ormOptions);
    }
}

class MainTests  {
    list: Array<ITest>

    constructor() {
        this.list = Reflect.ownKeys(this.__proto__)
            .filter(x => x.startsWith('test'))
            .map(x => {
                return {
                    id: x.substr(4),
                    func: this[x],
                    status: 'Not started 🫥'
                }
            })
    }

    async testBasicCollectionCrud(): Promise<string> {
        let coll: Collection;
        coll = new Collection(null, new Toucher(), TestInstance);
        coll.add(new TestInstance({$pk: '1', name: 'foo'}))
        coll.add(new TestInstance({$pk: '2', name: 'bar'}))

        const item = coll.get('2', '1', '4');
        if (!item) return 'Item not returned'
        if (item.length !== 3) return '3 items requested, got ' + item.join(', ');
        if (!item[0]) return 'Empty result'
        if (item[0].name !== 'bar') return 'Item name is not the stored one'
    }
    async testObjectIdentity() {
        const orm = new Orm(ormOptions);
        const Alone = await orm.getModel('Alone')
        const alone = new Alone({name: 'A'})
        const saved = await alone.$save()
        if (!saved.$pk) {
            return 'Saved object is not saved';
        }
        if (saved.name !== 'A') {
            return 'the returned object differs from the original'
        }
        if (!alone.$pk) {
            return 'Object created and not saved';
        }
        if (alone.$pk !== saved.$pk) {
            return 'Saved and sent have different $PK';
        }
        const a = await orm.get('Alone', alone.$pk)
        if (a.$pk !== saved.$pk) {
            return 'The get returned different object'
        }
        alone.name = 'Foo';
        if (saved.name !== 'Foo') {
            return 'Saved and returned are not the same object';
        }
        const b = orm.resources.getCollection('Alone').get(alone.$pk)[0];
        if (b.name !== alone.name) {
            return 'The saved object generates a new instance';
        }
        if (a.name !== saved.name) {
            return 'Got and returned are not the same object';
        }
    }
    async testAloneCRUD() {
        const orm = new Orm(ormOptions);
        const Alone = await orm.getModel('Alone')
        await Alone.deleteAll()
        const alone = new Alone({name: 'B'})
        const saved = await alone.$save()
        const got = await orm.get('Alone', alone.$pk);
        got.name = 'Bar';
        await got.$save();
        if (saved.name !== 'Bar') {
            return 'Saved object didnt affect the in-memory one.'
        }
        let lastItem = await orm.get('Alone', saved.$pk);
        if (!lastItem) {
            return 'Item not updated'
        }
        await got.$delete();
        const item = await orm.get('Alone', 1);
        if (item) {
            return 'Delete didnt work';
        }
    }
    async testOneAndMoreGet() {
        const orm = new Orm(ormOptions);
        const Alone = await orm.getModel('Alone')
        await Alone.deleteAll()
        await (new Alone({name: 'Test', score: 20})).$save();
        await (new Alone({name: 'Test 2', score: 20})).$save();
        const item = await orm.get('Alone', 1);
        if (!(item.constructor === Alone)) {
            return 'Individual get didnt return individual object';
        }
        const items = await orm.get('Alone', [1,2]);
        if (!(items.constructor === Array)) {
            return 'Array of ids didnt return an array of objects';
        }
    }
    async testManyToOne() {
        const orm = window.orm = new Orm(ormOptions);
        const Master = await orm.getModel('Master')
        const Detail = await orm.getModel('Detail')
        await Master.deleteAll()
        await Detail.deleteAll()

        const master = new Master({name: 'A', score: 2.3, description: 'The first Master item'});
        await master.$save();
        let detail = new Detail({name: 'A1', score: 3.2, description: 'A 1 child', master_id: master.id});
        await detail.$save();
        detail = new Detail({name: 'A1', score: 3.2, description: 'A 1 child', master_id: master.id});
        await detail.$save();
        const orm2 = new Orm(ormOptions);
        const dd = await orm2.get('Detail', 1);
        console.log(dd.master)
        let result: IResource
        for (let i = 0; i < 10; i ++) {
            await sleep(100);
            result = dd.master
            if (result)
                break
        }
        if (!result)
            return 'No master found';
        if (result.$pk !== dd.master_id)
            return "It's not the right master"
        if (!result.name.startsWith('A'))
            return 'This master does not belong to the detail'
        console.log(result.details);
    }
    async testPager() {
        const orm = await fixtures.alones(10);
        const Alone = await orm.getModel('Alone');
        const pagerNF = orm.resources.getCollection('Alone')
            .getPager({});
        pagerNF.get(0, 10);
        await sleep(100);
        let pks = pagerNF.get(5, 10);
        console.log('Add 1 item via $save');
        const alone = new Alone({name: 'alone 11', score: 11, description: 'The first alone item'});
        const alones = await orm.get('Alone', range(11));
        await alone.$save();
        while (pagerNF.newBasket.length === 0)
            await sleep(50);
        let newPks = pagerNF.get(5, 10);
        if (!arrayEqual(pks, newPks))
            return 'Change done ahead of time';
        console.log(pagerNF.get(5, 10));
    }
    async testRSet() {
        const orm = new Orm(ormOptions);
        const Master = await orm.getModel('Master');
        const rset = new RSet(orm.resources, 'Master', {name: ['A']});
        console.log(rset.items);
        await sleep(100);
        console.log(rset.items)
        await sleep(100);
        console.log(rset.items)
        const items = rset.items;
        if (!items)
            return "rset didn't return items";
        if (!Array.isArray(items))
            return "Item returned by the RSet is not array";
        if (items[0].constructor !== Master)
            return "The RSet items didn't return array of Master";
    }
    async testMassiveCRUD() {
        const orm = new Orm(ormOptions);
        const Alone = await orm.getModel('Alone');
        await Alone.deleteAll();
        const alones = [];
        const numItems = 300;
        for (let i = 0; i < numItems; i ++) {
            alones.push(new Alone({name: `Alone ${i}`, score: i}));
        }
        const saved = await orm.saveBulk(alones);
        if (!saved)
            return "`saveBulk` didn't rerturn"
        if (saved.length !== numItems)
            return "`saveBulk` returned less items"
        const items = await orm.get('Alone', [2, 4, 6])
        if (!items)
            return 'No items returned'
        if (!Array.isArray(items))
            return 'The `orm.get` didnt return an array'
        if (items.length !== 3)
            return "The `orm.get` didn't return the exact number of items"
        if (!items.every(x => x && (x.constructor === Alone)))
            return "The `orm.get` didn't return the correct class items"
        const alone = await Alone.get(saved[3].$pk)
        if (alone.name !== saved[3].name)
            return "The one got is not the one set"
        const mixed = [];
        for (let i = Math.floor(numItems / 2); i < numItems; i ++) {
            saved[i].name += ' --- updated';
            mixed.push(saved[i]);
        }
        for (let i = 0; i < Math.floor(numItems / 2); i ++) {
            mixed.push(new Alone({name: `New Alone ${i + 1000}`}))
        }
        const reSaved = await orm.saveBulk(mixed)
        if (reSaved.filter(x => x.name.endsWith('updated')).length !== Math.floor(numItems / 2))
            return "not all got saved"
        if (saved[1].name.endsWith('updated'))
            return "Same instance violation"
        if (!saved[Math.floor(numItems / 2)].name.endsWith('updated'))
            return "Same instance violation"
        const deleted = await orm.delete(...saved)
        console.log(deleted)
        await Alone.deleteAll();
    }
    async testPagerSync() {
        const numItems = 500;
        const orm = await fixtures.alones(numItems);
        const Alone = await orm.getModel('Alone')
        const rset = new RSet(orm.resources, 'Alone', {}, ['id'], 21);
        let page = await rset.fetch()
        if (!page)
            return "RSet didn't fetch"
        if (!Array.isArray(page))
            return "RSet didn't return an array"
        if (page.length !== rset.rpp)
            return "Not all items were fetched"
        if (!page.every(x => x.id <= rset.rpp))
            return "RSet non properly sorted"
        for (let i = 1; i < (1 + Math.floor(numItems / rset.rpp)); i ++) {
            rset.page = i;
            page = await rset.setPage(i).fetch()
            if (!page.every(x => (x.id > (rset.rpp * (rset.page - 1)) && (x.id <= (rset.rpp * rset.page)))))
                return `Page ${i} is not fetched properly`
        }
        rset.page ++;
        page = await rset.fetch()
        if (page.length >= rset.rpp)
            return "Last page is longer than it should"
        await Alone.deleteAll()
    }
    async testPagerASync() {
        const numItems = 300
        const orm = await fixtures.alones(numItems);
        const Alone = await orm.getModel('Alone')
        const rset = new RSet(orm.resources, 'Alone', {}, ['id'], 21);
        let page = rset.items
        await sleep(100);
        page = rset.items
        await sleep(100);
        page = rset.items
        await sleep(100);
        page = rset.items
        if (!page)
            return "RSet didn't fetch"
        if (!Array.isArray(page))
            return "RSet didn't return an array"
        if (page.length !== rset.rpp)
            return "Not all items were fetched"
        if (!page.every(x => x.id <= rset.rpp))
            return "RSet non properly sorted"
        for (let i = 1; i < (1 + Math.floor(numItems / rset.rpp)); i ++) {
            rset.page = i;
            page = rset.setPage(i).items;
            await sleep(100);
            page = rset.setPage(i).items;
            if (!page.every(x => (x.id > (rset.rpp * (rset.page - 1)) && (x.id <= (rset.rpp * rset.page)))))
                return `Page ${i} is not fetched properly`
        }
        rset.page ++;
        page = rset.items;
        await sleep(100);
        page = rset.items;
        if (page.length >= rset.rpp)
            return "Last page is longer than it should"
        await Alone.deleteAll()
    }
    async testPagerHydratation() {
        const orm = await fixtures.alones(300);
        const Alone = await orm.getModel('Alone');
        const rset = new RSet((await orm).resources, 'Alone', {score: [2]});
        let page = await rset.fetch();
        console.log(page);
        const score2 = page ? page.length : 0;
        const saved = await orm.saveBulk(
            [..._.range(10).map(x => new Alone({name: 'cippa', score: 2, id: x + 1})),
                ..._.range(10).map(x => new Alone({name: 'cippa', score: 3, id: x + 40}))]);
        page = await rset.fetch();
        console.log(page)
        if (page.length !== 10)
            return "I'm expecting 10 record on the page. Filter didn't work thus I got " + page.length
    }
    async testRSetInsert1() {
        const orm = await fixtures.alones(260);
        const rset = new RSet(orm.resources, 'Alone', {name: 'Alone 4'})
        let page = await rset.setRpp(5).setPage(1).fetch()
        let scores = page.map(x => x.score);
        if (![2, 7, 12, 17, 22].every(x => scores.includes(x)))
            return 'Incorrect score'
        page = await rset.setSort(['~score']).fetch()
        scores = page.map(x => x.score)
        console.log(scores)
        if (![127, 122, 117, 112, 107].every(x => scores.includes(x)))
            return 'Incorect page sorting';
    }
    async testExternalHydratation() {
        const orm = await fixtures.alones(300);
        const rset = await orm.query('Alone', {score: [4]}, ['name'])
        const items = rset.items
        for (let x = 0;x < 10; x ++) {
            if (items.length === 0)
                await sleep(50)
        }
        if (items.length === 0)
            return 'Records where not propagated externally';
    }
    async testCreateTodos() {
        const Todo = await orm.getModel('Todo');
        await orm.saveBulk(range(300).map(x => new Todo({
            title: `Todo ${x + 1}`,
            description: `Description ${x + 1}`,
        })));
    }
}

export default MainTests