import {Setor} from './setor.model'

export class Pesquisa {
    constructor(
        public localidade?: string,
        public cargo?: string,
        public qtd = 10,
        public setores?: Setor[]
    ) {}
}
