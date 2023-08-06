"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const utils_1 = require("../../../common/utils");
const chaiAsPromised = require("chai-as-promised");
const amlClient_1 = require("../aml/amlClient");
describe('Unit Test for amlClient', () => {
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('test parseContent', async () => {
        let amlClient = new amlClient_1.AMLClient('', '', '', '', '', '', '', '');
        chai.assert.equal(amlClient.parseContent('test', 'test:1234'), '1234', "The content should be 1234");
        chai.assert.equal(amlClient.parseContent('test', 'abcd:1234'), '', "The content should be null");
    });
});
