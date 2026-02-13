
export interface ITest {
    func: Function,
    id: string,
    status: string,
    error?:string,
}

const fixtures = {
    zeroProviders(orm: Orm)  {
        
    }
};

export class MainTests  {
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

    async testObjectIdentity() {
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
        const b = orm.resources.getCollection('Alone').get(alone.$pk);
        if (b.name !== alone.name) {
            return 'The saved object generates a new instance';
        }
        if (a.name !== saved.name) {
            return 'Got and returned are not the same object';
        }
    }
    async testAloneCRUD() {
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
        if (await orm.get('Alone', 1)) {
            return 'Delete didnt work';
        }
    }
    async testOneAndMoreGet() {
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

    async testRSetBasic() {
        const Alone = await orm.getModel('Alone')
        await Alone.deleteAll()
        await (new Alone({name: 'Test', score: 20})).$save();
        await (new Alone({name: 'Test 2', score: 20})).$save();

        const items = await orm.query('Alone', {name: 'Test'})
        if (items.constructor.name !== 'RSet') {
            return 'Query didnt return am RSet';
        }
    }
}