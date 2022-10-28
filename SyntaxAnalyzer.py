from Token import Token


class SyntaxAnalyzer:
    current_index: int = 0
    end_index: int = 0
    token_set: list[Token] = []

    @staticmethod
    def main(token_set: list[Token]):
        SyntaxAnalyzer.end_index = len(token_set) - 1
        SyntaxAnalyzer.token_set = token_set
        if(SyntaxAnalyzer.validate()):
            return "Syntax Valid"
        return f'Invalid Syntax @ line # {token_set[SyntaxAnalyzer.current_index].line_number}'

    @staticmethod
    def validate() -> bool:
        if(SyntaxAnalyzer.s() and SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "end_marker"):
            return True
        return False

    @staticmethod
    def s() -> bool:
        # ? selection_set => {DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            if(SyntaxAnalyzer.sst() and SyntaxAnalyzer.s()):
                return True
        # ? selection_set => {final, static, abstract, class, function}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier', 'class', 'function']):
            if(SyntaxAnalyzer.defs() and SyntaxAnalyzer.s()):
                return True
        # ? selection_set => { $ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'end_marker'):
            return True

        return False

    @staticmethod
    def defs() -> bool:
        # ? selection_set => {final, static, abstract, class}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier', 'class']):
            if(SyntaxAnalyzer.class_def() and SyntaxAnalyzer.def1()):
                return True
        # ? selection_set => {function}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'function'):
            if(SyntaxAnalyzer.func_def() and SyntaxAnalyzer.def1()):
                return True

        return False

    @staticmethod
    def def1() -> bool:
        # ? selection_set => {final, static, abstract, class, function}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier', 'class', 'function']):
            if(SyntaxAnalyzer.defs()):
                return True
        # ? selection_set => {DT, ID, while, for, if, return, break, continue, pass, final, static, abstract, class, function, $}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if', 'return', 'jump_statements', 'type_modifier', 'class', 'function', 'end_marker']):
            return True

        return False

    @staticmethod
    def decl() -> bool:
        # ? selection_set => {DT}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'data_type'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.a()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.list()):
                        return True

        return False

    @staticmethod
    def a() -> bool:
        # ? selection_set => { [] }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'arr_dec'):
            SyntaxAnalyzer.current_index += 1
            return True
        # ? selection_set => {ID}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            return True

        return False

    @staticmethod
    def list() -> bool:
        # ? selection_set => { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ','):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.decl()):
                return True
        # ? selection_set => { ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
            SyntaxAnalyzer.current_index += 1
            return True
        # ? selection_set => { = }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'assignment'):
            if(SyntaxAnalyzer.init()):
                return True

        return False

    @staticmethod
    def init() -> bool:
        # ? selection_set => { = }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'assignment'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'new'):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'data_type'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '['):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.p()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ']'):
                                SyntaxAnalyzer.current_index += 1
                                return True
        # ? selection_set => { ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
            return True

        return False

    @staticmethod
    def fn_call() -> bool:
        # ? selection_set => {ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.p()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.end()):
                            return True
        return False

    @staticmethod
    def end() -> bool:
        # ? selection_set => { ; }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
            SyntaxAnalyzer.current_index += 1
            return True
        # ? selection_set => {DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def p() -> bool:
        # ? selection_set => {this, super, ID, constant, ( , ! }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super', 'identifier', 'number', '(', 'not_operator']):
            if(SyntaxAnalyzer.oe() and SyntaxAnalyzer.p1()):
                return True
        # ? selection_set => { ) , ] }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [')', ']']):
            return True

        return False

    # TODO: check
    @staticmethod
    def p1() -> bool:
        # ? selection_set => { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ','):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.oe() and SyntaxAnalyzer.p1()):
                return True
        # ? selection_set => { ), ] }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
            return True

        return False

    @staticmethod
    def func_def() -> bool:
        # ? selection_set => {function}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'function'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.fdt1()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.para()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.mst() and SyntaxAnalyzer.return_st()):
                                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                            SyntaxAnalyzer.current_index += 1
                                            return True

        return False

    @staticmethod
    def fdt() -> bool:
        # ? selection_set => {DT}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'data_type'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.a()):
                return True
        # ? selection_set => {ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.a()):
                return True

        return False

    @staticmethod
    def fdt1() -> bool:
        # ? selection_set => {DT, ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier']):
            if(SyntaxAnalyzer.fdt()):
                return True
        # ? selection_set => { void }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
            SyntaxAnalyzer.current_index += 1
            return True

        return False

    @staticmethod
    def para() -> bool:
        # ? selection_set => {DT, ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier']):
            if(SyntaxAnalyzer.fdt()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.s_para()):
                        return True
        # ? selection_set => { ) }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
            return True

        return False

    @staticmethod
    def s_para() -> bool:
        # ? selection_set => {  ,  }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ','):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.fdt()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.s_para()):
                        return True
        # ? selection_set => { ) }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
            return True

        return False

    @staticmethod
    def while_st() -> bool:
        # ? selection_set => {while}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'while'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.oe()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.mst()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                    SyntaxAnalyzer.current_index += 1
                                    return True

        return False

    @staticmethod
    def for_st() -> bool:
        # ? selection_set => {for}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'for'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign_st() and SyntaxAnalyzer.oe()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.inc_dec_st()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.mst()):
                                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                            SyntaxAnalyzer.current_index += 1
                                            return True

        return False

    @staticmethod
    def inc_dec_st() -> bool:
        # ? selection_set => {ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.common() and SyntaxAnalyzer.inc_dec_opr()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                    SyntaxAnalyzer.current_index += 1
                    return True
        # ? selection_set => { ++ , -- }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'inc_dec'):
            if(SyntaxAnalyzer.inc_dec_opr()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.common()):
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                            SyntaxAnalyzer.current_index += 1
                            return True
        return False

    @staticmethod
    def inc_dec_opr() -> bool:
        # ? selection_set => {++ , -- }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'inc_dec_opr'):
            SyntaxAnalyzer.current_index += 1
            return True

        return False

    @staticmethod
    def common() -> bool:
        # ? selection_set => { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.common()):
                    return True
        # ? selection_set => { ( }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.p()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.common()):
                            return True
        # ? selection_set => { [ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '['):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.oe()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ']'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.common1()):
                        return True
        # ? selection_set => {++ , -- , ; , = , CO}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['inc_dec', 'EOL', 'assignment', 'compound_assignment']):
            return True

        return False

    @staticmethod
    def common1() -> bool:
        # ? selection_set => { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.common()):
                    return True
        # ? selection_set => {++ , -- , ; , = , CO}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['inc_dec', 'EOL', 'assignment', 'compound_assignment']):
            return True

        return False

    @staticmethod
    def sst() -> bool:
        # ? selection_set => {DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            if(SyntaxAnalyzer.decl() or SyntaxAnalyzer.while_st() or SyntaxAnalyzer.for_st() or SyntaxAnalyzer.if_st() or SyntaxAnalyzer.error_handle() or SyntaxAnalyzer.afci()):
                return True

        return False

    @staticmethod
    def afci() -> bool:
        # ? selection_set => {ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.afci1()):
                return True
        # ? selection_set => { ++ , -- }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'inc_dec'):
            if(SyntaxAnalyzer.inc_dec_opr()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.common()):
                        return True

        return False

    @staticmethod
    def afci1() -> bool:
        # ? selection_set => { [ }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '['):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.oe()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ']'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.common1() and SyntaxAnalyzer.afci2()):
                        return True
        # ? selection_set => { . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.common() and SyntaxAnalyzer.afci2()):
                return True
        # ? selection_set => { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.p()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.afci3()):
                        return True
        # ? selection_set => { ++ , -- , = , CO }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['inc_dec', ' assignment', 'compound_assignment']):
            return True

        return False

    @staticmethod
    def afci2() -> bool:
        # ? selection_set => { ++ , -- }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'inc_dec'):
            if(SyntaxAnalyzer.inc_dec_opr()):
                return True
        # ? selection_set => { = , CO }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['assignment', 'compound_assignment']):
            if(SyntaxAnalyzer.assign_opr() and SyntaxAnalyzer.oe()):
                return True
        return False

    @staticmethod
    def afci3() -> bool:
        # ? selection_set => {DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            if(SyntaxAnalyzer.end()):
                return True
        # ? selection_set => { . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.common() and SyntaxAnalyzer.afci2()):
                return True

        return False

    @staticmethod
    def mst() -> bool:
        # ? selection_set => {DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            if(SyntaxAnalyzer.sst() and SyntaxAnalyzer.mst()):
                return True
        # ? selection_set => { } , public, sealed, static, function, construct, DT, ID, while, for, if}
        # ! we have no construct. only static can come?
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['}', 'access_modifier', 'type_modifier', 'function' 'data_type', 'identifier', 'while', 'for', 'if']):
            return True
        return False

    @staticmethod
    def if_st() -> bool:
        # ? selection_set => {if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'if'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                if(SyntaxAnalyzer.oe()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.if_body()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.furthermore_st() and SyntaxAnalyzer.else_st()):
                                        return True

        return False

    @staticmethod
    def furthermore_st() -> bool:
        # ? selection_set => {furthermore}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'furthermore'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                if(SyntaxAnalyzer.oe()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.if_body()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.furthermore_st()):
                                        return True
        # ? selection_set => {else, DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['else', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def else_st() -> bool:
        # ? selection_set => {else}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'else'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.if_body()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                        SyntaxAnalyzer.current_index += 1
        # ? selection_set => {DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def assign_st() -> bool:
        # ? selection_set => {ID}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.common() and SyntaxAnalyzer.assign_opr() and SyntaxAnalyzer.oe()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                    SyntaxAnalyzer.current_index += 1
                    return True

        return False

    @staticmethod
    def assign_opr() -> bool:
        # ? selection_set => { = , CO }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['assignment', 'compound_assignment']):
            SyntaxAnalyzer.current_index += 1
            return True

        return False

    @staticmethod
    def oe() -> bool:
        # ? selection_set => {this , super ,ID, (,!, constant }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super', 'identifier', '(', 'not_operator', 'number']):
            if(SyntaxAnalyzer.ae() and SyntaxAnalyzer.oe1()):
                return True

        return False

    @staticmethod
    def oe1() -> bool:
        # ? selection_set => { || }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'or_operator'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.ae() and SyntaxAnalyzer.oe1()):
                return True
        # ? selection_set => { ), ], ; ,DT, ID, while, for, if }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def ae() -> bool:
        # ? selection_set => { this , super ,ID, (, !, constant }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super', 'identifier', '(', 'not_operator', 'number']):
            if(SyntaxAnalyzer.re() and SyntaxAnalyzer.ae1()):
                return True

        return False

    @staticmethod
    def ae1() -> bool:
        # ? selection_set => { && }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'and_operator'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.re() and SyntaxAnalyzer.ae1()):
                return True
        # ? selection_set => { ||, ), ], ; ,DT, ID, while, for, if }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['or_operator', ')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def re() -> bool:
        # ? selection_set => {this , super ,ID, (, !, constant}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super', 'identifier', '(', 'not_operator', 'number']):
            if(SyntaxAnalyzer.e() and SyntaxAnalyzer.re1()):
                return True

        return False

    @staticmethod
    def re1() -> bool:
        # ? selection_set => {RO}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'relational_operators'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.e() and SyntaxAnalyzer.re1()):
                return True
        # ? selection_set => { && , ||, ), ], ; ,DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['and_operator', 'or_operator', ')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def e() -> bool:
        # ? selection_set => {this , super ,ID, (, !, constant}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super', 'identifier', '(', 'not_operatotr', 'number']):
            if(SyntaxAnalyzer.t() and SyntaxAnalyzer.e1()):
                return True

        return False

    @staticmethod
    def e1() -> bool:
        # ? selection_set => {PM}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'plus_minus'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.t() and SyntaxAnalyzer.e1()):
                return True
        # ? selection_set => { RO, && , ||, ), ], ; ,DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['relational_operators', 'and_operator', 'or_operator', ')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def t() -> bool:
        # ? selection_set => {this , super ,ID, (, !, constant}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super', 'identifier', '(', 'not_operator', 'number']):
            if(SyntaxAnalyzer.f() and SyntaxAnalyzer.t1()):
                return True

        return False

    @staticmethod
    def t1():
        # ? selection_set => {MDM}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'multiply_divide_mod'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.f() and SyntaxAnalyzer.t1()):
                return True
        # ? selection_set => { PM, RO, && , ||, ), ], ; ,DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['plus_minus', 'relational_operators', 'and_operator', 'or_operator', ')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def f() -> bool:
        # ? selection_set => {this, super}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super']):
            if(SyntaxAnalyzer.ts()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.opts()):
                        return True
        # ? selection_set => {ID}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.opts()):
                return True
        # ? selection_set => { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.oe()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                    SyntaxAnalyzer.current_index += 1
                    return True
        # ? selection_set => { ! }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'not_operator'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.f()):
                return True
        # ? selection_set => { constant }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'number'):
            SyntaxAnalyzer.current_index += 1
            return True

        return False

    @staticmethod
    def ts() -> bool:
        # ? selection_set => {this, super}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['this', 'super']):
            SyntaxAnalyzer.current_index += 1
            return True

        return False

    @staticmethod
    def opts() -> bool:
        # ? selection_set => { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.opts()):
                    return True
        # ? selection_set => { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.p()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.opts()):
                                return True
        # ? selection_set => { [ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '['):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.oe()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ']'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.opts1()):
                        return True
        # ? selection_set => {MDM, PM, RO, && , ||, ), ], ; ,DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['multiply_divide_mod', 'plus_minus', 'relational_operators', 'and_operator', 'or_operator', ')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def opts1() -> bool:
        # ? selection_set => { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.opts()):
                    return True
        # ? selection_set => {MDM, PM, RO, && , ||, ), ], ; ,DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['multiply_divide_mod', 'plus_minus', 'relational_operators', 'and_operator', 'or_operator', ')', ']', 'EOL', 'data_type', 'identifier', 'while', 'for', 'if']):
            return True

        return False

    @staticmethod
    def class_def() -> bool:
        # ? selection_set => { final, static, abtract, class }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier', 'class']):
            if(SyntaxAnalyzer.tm()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'class'):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.inht()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.o_body()):
                                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                        SyntaxAnalyzer.current_index += 1
                                        return True

        return False

    @staticmethod
    def tm() -> bool:
        # ? selection_set => {final, static, abtract}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'type_modifier'):
            SyntaxAnalyzer.current_index += 1
            return True
        # ? selection_set => {class}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'class'):
            return True

        return False

    @staticmethod
    def inht() -> bool:
        # ? selection_set => {extends}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'extends'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'identifier'):
                SyntaxAnalyzer.current_index += 1
                return True
        # ? selection_set => { { }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
            return True

        return False

    @staticmethod
    def o_body() -> bool:
        # ? selection_set => {public, hidden}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'access_modifier'):
            if(SyntaxAnalyzer.am() and SyntaxAnalyzer.o_body1()):
                return True
        # ? selection_set => {DT, ID, while, for, if, static, function, abstract}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if', 'type_modifier', 'function']):
            if(SyntaxAnalyzer.mst() and SyntaxAnalyzer.o_body1()):
                return True
        # ? selection_set => {construct}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'construct'):
            if(SyntaxAnalyzer.constructor() and SyntaxAnalyzer.c_body()):
                return True
        # ? selection_set => { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
            return True

        return False

    @staticmethod
    def o_body1() -> bool:
        # ? selection_set => {static, function}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier', 'function']):
            if(SyntaxAnalyzer.sta() and SyntaxAnalyzer.func_def() and SyntaxAnalyzer.c_body() and SyntaxAnalyzer.o_body2()):
                return True
        # ? selection_set =>  {abstract}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "type_modifier"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.func_def() and SyntaxAnalyzer.a_body()):
                return True

        return False

    @staticmethod
    def o_body2() -> bool:
        # ? selection_set => = {public, hidden, DT, ID, while, for, if}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['access_modifier', 'data_type', 'identifier', 'while', 'for', 'if']):
            if(SyntaxAnalyzer.a_body()):
                return True
        # ? selection_set => { } }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
            return True

        return False

    @staticmethod
    def c_body() -> bool:
        # ? selection_set => {public, hidden}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['access_modifier']):
            if(SyntaxAnalyzer.am() and SyntaxAnalyzer.sta() and SyntaxAnalyzer.func_def() and SyntaxAnalyzer.c_body()):
                return True
        # ? selection_set => {DT, ID, while, for, if}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if']):
            if(SyntaxAnalyzer.sst() and SyntaxAnalyzer.mst() and SyntaxAnalyzer.c_body()):
                return True
        # ? selection_set => {construct}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'construct'):
            if(SyntaxAnalyzer.constructor() and SyntaxAnalyzer.c_body()):
                return True

        return False

    @staticmethod
    def sta() -> bool:
        # ? selection_set => {static}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'type_modifier'):
            return True
        # ? selection_set => {function}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'function'):
            return True

        return False

    @staticmethod
    def constructor() -> bool:
        # ? selection_set => {construct}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'construct'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.para()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '{'):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.con_body()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
                                    SyntaxAnalyzer.current_index += 1
        return False

    @staticmethod
    def con_body() -> bool:
        # ? selection_set => {super}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'super'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.d()):
                return True
        # ? selection_set => {this}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'this'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.b()):
                return True

        return False

    @staticmethod
    def d() -> bool:
        # ? selection_set => {   .  }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.fn_call()):
                return True
        # ? selection_set => { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '('):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.p()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
                    SyntaxAnalyzer.current_index += 1

        return False

    @staticmethod
    def b() -> bool:
        # ? selection_set => {   .  }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '.'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.assign_st()):
                return True

        return False

    @staticmethod
    def a_body() -> bool:
        # ? selection_set => {public, hidden, abstract}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['access_modifier', 'type_modifier']):
            if(SyntaxAnalyzer.am() and SyntaxAnalyzer.a_body1()):
                return True
        # ? selection_set => {public, hidden, static, function, DT, ID, while, for, if, construct}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['access_modifier', 'type_modifier', 'function', 'data_type', 'identifier', 'while', 'for', 'if', 'construct']):
            if(SyntaxAnalyzer.sst() and SyntaxAnalyzer.mst() and SyntaxAnalyzer.a_body()):
                return True
        # ? selection_set =>  { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == '}'):
            return True

        return False

    @staticmethod
    def a_body1() -> bool:
        # ? selection_set => {static , function}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier', 'function']):
            if(SyntaxAnalyzer.sta() and SyntaxAnalyzer.func_def() and SyntaxAnalyzer.a_body()):
                return True
        # ? selection_set => {abstract}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['type_modifier']):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.func_def() and SyntaxAnalyzer.a_body()):
                return True

        return False

    @staticmethod
    def if_body() -> bool:
        # ? selection_set => {DT, ID, while, for, if, break, continue, pass}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['data_type', 'identifier', 'while', 'for', 'if', 'jump_statements']):
            if(SyntaxAnalyzer.mst() and SyntaxAnalyzer.if_sst()):
                return True

        return False

    @staticmethod
    def if_sst() -> bool:
        # ? selection_set => {break, continue, pass}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'jump_statements'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                SyntaxAnalyzer.current_index += 1
                return True
        # ? selection_set => { ) }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ')'):
            return True

        return False

    @staticmethod
    def return_st() -> bool:
        # ? selection_set =>  {return}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'return'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.return_st1()):
                return True

        return False

    @staticmethod
    def return_st1() -> bool:
        # ? selection_set => {bool }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'bool'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                SyntaxAnalyzer.current_index += 1
                return True
        # ? selection_set => {const}
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'number'):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'EOL'):
                SyntaxAnalyzer.current_index += 1
                return True

        return False

    @staticmethod
    def am() -> bool:
        # ? selection_set => {access_modifier}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == 'access_modifier'):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def error_handle() -> bool:
        # TODO implementation left
        return False

# ! correct cfgs and their implementation
# ! check complete code
