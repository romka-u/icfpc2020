/**
 *    author:  tourist
 *    created: 18.07.2020 12:34:33       
**/
#undef _GLIBCXX_DEBUG

#include <bits/stdc++.h>

using namespace std;

template <typename A, typename B>
string to_string(pair<A, B> p);

template <typename A, typename B, typename C>
string to_string(tuple<A, B, C> p);

template <typename A, typename B, typename C, typename D>
string to_string(tuple<A, B, C, D> p);

string to_string(const string& s) {
  return '"' + s + '"';
}

string to_string(const char* s) {
  return to_string((string) s);
}

string to_string(bool b) {
  return (b ? "true" : "false");
}

string to_string(vector<bool> v) {
  bool first = true;
  string res = "{";
  for (int i = 0; i < static_cast<int>(v.size()); i++) {
    if (!first) {
      res += ", ";
    }
    first = false;
    res += to_string(v[i]);
  }
  res += "}";
  return res;
}

template <size_t N>
string to_string(bitset<N> v) {
  string res = "";
  for (size_t i = 0; i < N; i++) {
    res += static_cast<char>('0' + v[i]);
  }
  return res;
}

template <typename A>
string to_string(A v) {
  bool first = true;
  string res = "{";
  for (const auto &x : v) {
    if (!first) {
      res += ", ";
    }
    first = false;
    res += to_string(x);
  }
  res += "}";
  return res;
}

template <typename A, typename B>
string to_string(pair<A, B> p) {
  return "(" + to_string(p.first) + ", " + to_string(p.second) + ")";
}

template <typename A, typename B, typename C>
string to_string(tuple<A, B, C> p) {
  return "(" + to_string(get<0>(p)) + ", " + to_string(get<1>(p)) + ", " + to_string(get<2>(p)) + ")";
}

template <typename A, typename B, typename C, typename D>
string to_string(tuple<A, B, C, D> p) {
  return "(" + to_string(get<0>(p)) + ", " + to_string(get<1>(p)) + ", " + to_string(get<2>(p)) + ", " + to_string(get<3>(p)) + ")";
}

void debug_out() { cerr << endl; }

template <typename Head, typename... Tail>
void debug_out(Head H, Tail... T) {
  cerr << " " << to_string(H);
  debug_out(T...);
}

#ifdef LOCAL
#define debug(...) cerr << "[" << #__VA_ARGS__ << "]:", debug_out(__VA_ARGS__)
#else
#define debug(...) 42
#endif

struct Node;

map<string, Node*> functions;

Node* MakeNode(string text);
Node* MakeNode(string text, Node* left, Node* right);
Node* Demodulate(string modulated);

struct Node {
  string text;
  Node* left;
  Node* right;

  Node* eval() {
    while (true) {
      if (left != nullptr) {
        left->eval();
      }
//      debug(repr());
      Node* cur = this;
      int aps = 0;
      while (cur->text == "ap") {
        cur = cur->left;
        ++aps;
      }
      if (cur->text == "add") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x0 = this->left->right;
          Node* x1 = this->right;
          x0->eval();
          x1->eval();
          this->text = to_string(x0->get_number() + x1->get_number());
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "mul") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x0 = this->left->right;
          Node* x1 = this->right;
          x0->eval();
          x1->eval();
          this->text = to_string(x0->get_number() * x1->get_number());
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "div") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x0 = this->left->right;
          Node* x1 = this->right;
          x0->eval();
          x1->eval();
          this->text = to_string(x0->get_number() / x1->get_number());
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "neg") {
        assert(aps <= 1);
        if (aps == 1) {
          Node* x0 = this->right;
          x0->eval();
          this->text = to_string(-x0->get_number());
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "eq") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x0 = this->left->right;
          Node* x1 = this->right;
          x0->eval();
          x1->eval();
          if (x0->get_number() == x1->get_number()) {
            this->text = "t";
          } else {
            this->text = "f";
          }
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "lt") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x0 = this->left->right;
          Node* x1 = this->right;
          x0->eval();
          x1->eval();
          if (x0->get_number() < x1->get_number()) {
            this->text = "t";
          } else {
            this->text = "f";
          }
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "s") {
        assert(aps <= 3);
        if (aps == 3) {
          Node* x0 = this->left->left->right;
          Node* x1 = this->left->right;
          Node* x2 = this->right;
          this->text = "ap";
          this->left = MakeNode("ap", x0, x2);
          this->right = MakeNode("ap", x1, x2);
          continue;
        }
      }
      if (cur->text == "c") {
        assert(aps <= 3);
        if (aps == 3) {
          Node* x0 = this->left->left->right;
          Node* x1 = this->left->right;
          Node* x2 = this->right;
          this->text = "ap";
          this->left = MakeNode("ap", x0, x2);
          this->right = x1;
          continue;
        }
      }
      if (cur->text == "b") {
        assert(aps <= 3);
        if (aps == 3) {
          Node* x0 = this->left->left->right;
          Node* x1 = this->left->right;
          Node* x2 = this->right;
          this->text = "ap";
          this->left = x0;
          this->right = MakeNode("ap", x1, x2);
          continue;
        }
      }
      if (cur->text == "t") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x0 = this->left->right;
          x0->eval();
          this->text = x0->text;
          this->left = x0->left;
          this->right = x0->right;
          continue;
        }
      }
      if (cur->text == "f") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x1 = this->right;
          x1->eval();
          this->text = x1->text;
          this->left = x1->left;
          this->right = x1->right;
          continue;
        }
      }
      if (cur->text == "i" || cur->text == "modem" || cur->text == "multipledraw") {
        assert(aps <= 1);
        if (aps == 1) {
          Node* x0 = this->right;
          x0->eval();
          this->text = x0->text;
          this->left = x0->left;
          this->right = x0->right;
          continue;
        }
      }
      if (cur->text == "cons" || cur->text == "vec") {
        assert(aps <= 3);
        if (aps == 3) {
          Node* x0 = this->left->left->right;
          Node* x1 = this->left->right;
          Node* x2 = this->right;
          this->text = "ap";
          this->left = MakeNode("ap", x2, x0);
          this->right = x1;
          continue;
        }
      }
      if (cur->text == "car") {
        assert(aps <= 1);
        if (aps == 1) {
          Node* x2 = this->right;
          this->text = "ap";
          this->left = x2;
          this->right = MakeNode("t");
          continue;
        }
      }
      if (cur->text == "cdr") {
        assert(aps <= 1);
        if (aps == 1) {
          Node* x2 = this->right;
          this->text = "ap";
          this->left = x2;
          this->right = MakeNode("f");
          continue;
        }
      }
      if (cur->text == "nil") {
        assert(aps <= 1);
        if (aps == 1) {
          this->text = "t";
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "isnil") {
        assert(aps <= 1);
        if (aps == 1) {
          Node* x = this->right;
          this->text = "ap";
          this->left = x;
          this->right = MakeNode("skip2f");
          continue;
        }
      }
      if (cur->text == "skip2f") {
        assert(aps <= 2);
        if (aps == 2) {
          this->text = "f";
          this->left = nullptr;
          this->right = nullptr;
          continue;
        }
      }
      if (cur->text == "if0") {
        assert(aps <= 3);
        if (aps == 3) {
          Node* xn = this->left->left->right;
          Node* x0 = this->left->right;
          Node* x1 = this->right;
          xn->eval();
          if (xn->get_number() == 0) {
            this->text = x0->text;
            this->left = x0->left;
            this->right = x0->right;
          } else {
            this->text = x1->text;
            this->left = x1->left;
            this->right = x1->right;
          }
          continue;
        }
      }
      if (cur->text == "interact") {
        assert(aps <= 3);
        if (aps == 3) {
          Node* x2 = this->left->left->right;
          Node* x4 = this->left->right;
          Node* x3 = this->right;
          this->text = "ap";
          this->left = MakeNode("ap", MakeNode("f38"), x2);
          this->right = MakeNode("ap", MakeNode("ap", x2, x4), x3);
          continue;
        }
      }
      if (cur->text == "f38") {
        assert(aps <= 2);
        if (aps == 2) {
          Node* x2 = this->left->right;
          Node* x0 = this->right;
          this->text = "ap";
          this->left = MakeNode("ap", MakeNode("ap", MakeNode("if0"), MakeNode("ap", MakeNode("car"), x0)),
                                      MakeNode("ap",
                                        MakeNode("ap", MakeNode("cons"), MakeNode("ap", MakeNode("modem"), MakeNode("ap", MakeNode("car"), MakeNode("ap", MakeNode("cdr"), x0)))),
                                        MakeNode("ap", MakeNode("ap", MakeNode("cons"), MakeNode("ap", MakeNode("multipledraw"), MakeNode("ap", MakeNode("car"), MakeNode("ap", MakeNode("cdr"), MakeNode("ap", MakeNode("cdr"), x0))))), MakeNode("nil"))));
          this->right = MakeNode("ap",
                          MakeNode("ap", MakeNode("ap", MakeNode("interact"), x2), MakeNode("ap", MakeNode("modem"), MakeNode("ap", MakeNode("car"), MakeNode("ap", MakeNode("cdr"), x0)))),
                          MakeNode("ap", MakeNode("send"), MakeNode("ap", MakeNode("car"), MakeNode("ap", MakeNode("cdr"), MakeNode("ap", MakeNode("cdr"), x0)))));
          continue;
        }
      }
      if (cur->text == "send") {
        assert(aps <= 1);
        if (aps == 1) {
          Node* x0 = this->right;
          x0->eval();
          debug(x0->repr());
          string to_send = x0->modulate();
//          debug(to_send);
          system(("curl -X POST \"https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=1242ae59bc9f4385b3c3eaa60764a09c\" -H  \"accept: */*\" -H  \"Content-Type: text/plain\" -d \"" + to_send + "\" >zcurlout 2>znul").c_str());
          string received;
          ifstream in("zcurlout");
          in >> received;
          in.close();
//          debug(received);
          Node* received_node = Demodulate(received);
          debug(received_node->repr());
          this->text = received_node->text;
          this->left = received_node->left;
          this->right = received_node->right;
          continue;
        }
      }
//      debug("break");
      break;
    }
    return this;
  }

  string repr(int depth = 0) {
    string ret = text;
    if (depth > 3 && left != nullptr) {
      ret += " ... ...";
      return ret;
    }
    if (left != nullptr) {
      ret += " ";
      ret += left->repr(depth + 1);
    }
    if (right != nullptr) {
      ret += " ";
      ret += right->repr(depth + 1);
    }
    return ret;
  }

  string modulate() {
    eval();
    if (text == "nil") {
      return "00";
    }
    if (text == "ap" && left->text == "ap" && (left->left->text == "cons" || left->left->text == "vec")) {
      Node* check = MakeNode("ap", MakeNode("isnil"), this);
      check->eval();
      assert(check->text == "f");
      Node* first = MakeNode("ap", MakeNode("car"), this);
      Node* tail = MakeNode("ap", MakeNode("cdr"), this);
      return "11" + first->modulate() + tail->modulate();
    }
    long long num = get_number();
    string ret = "";
    if (num >= 0) {
      ret += "01";
    } else {
      ret += "10";
      num = -num;
    }
    int bits = 0;
    {
      long long tmp = num;
      while (tmp > 0) {
        bits += 1;
        tmp >>= 1;
      }
    }
    bits = (bits + 3) / 4 * 4;
    ret += string(bits / 4, '1');
    ret += "0";
    for (int i = bits - 1; i >= 0; i--) {
      if (num & (1LL << i)) {
        ret += "1";
      } else {
        ret += "0";
      }
    }
    return ret;
  }

  string unlist() {
    eval();
/*    if (left != nullptr && left->left != nullptr) {
      debug(text, left->text, left->left->text);
      if (left->left->text == "send") {
        left->right->eval();
        debug(left->right->repr());
      }
    }*/
    if (text == "ap" && left->text == "ap" && (left->left->text == "cons" || left->left->text == "vec")) {
      Node* check = MakeNode("ap", MakeNode("isnil"), this);
      check->eval();
      assert(check->text == "f");
      Node* first = MakeNode("ap", MakeNode("car"), this);
      Node* tail = MakeNode("ap", MakeNode("cdr"), this);
      return "(" + first->unlist() + ", " + tail->unlist() + ")";
    }
    return text;
  }

  string unlist_ap() {
    eval();
/*    debug(repr());
    debug(text);
    if (left != nullptr) {
      debug(left->text);
      if (left->left != nullptr) {
        debug(left->left->text);
      }
    }*/
    if (text == "ap" && left->text == "ap" && (left->left->text == "cons" || left->left->text == "vec")) {
      Node* check = MakeNode("ap", MakeNode("isnil"), this);
      check->eval();
      assert(check->text == "f");
      Node* first = MakeNode("ap", MakeNode("car"), this);
      Node* tail = MakeNode("ap", MakeNode("cdr"), this);
      return "ap ap cons " + first->unlist_ap() + " " + tail->unlist_ap();
    }
    return text;
  }

  long long get_number() {
/*    if (text == "ap") {
      debug(repr(-5));
    }*/
    int ptr = 0;
    int sign = 1;
    if (text[ptr] == '-') {
      ++ptr;
      sign = -1;
    }
    long long num = 0;
    while (ptr < (int) text.size()) {
      assert(text[ptr] >= '0' && text[ptr] <= '9');
      num = num * 10 + (int) (text[ptr] - '0');
      ++ptr;
    }
    return num * sign;
  }
};

Node* MakeNode(string text) {
  if (text[0] == ':') {
    auto iter = functions.find(text);
    if (iter != functions.end()) {
      return iter->second;
    }
  }
  Node* ret = new Node();
  ret->text = text;
  ret->left = nullptr;
  ret->right = nullptr;
  if (text[0] == ':') {
    functions[text] = ret;
  }
  return ret;
}

Node* MakeNode(string text, Node* left, Node* right) {
  Node* ret = new Node();
  ret->text = text;
  ret->left = left;
  ret->right = right;
  return ret;
}

Node* Demodulate(string modulated) {
  int ptr = 0;
  function<Node*()> Dfs = [&]() {
    auto cur = modulated.substr(ptr, 2);
    ptr += 2;
    if (cur == "00") {
      return MakeNode("nil");
    }
    if (cur == "11") {
      Node* left = Dfs();
      Node* right = Dfs();
      return MakeNode("ap", MakeNode("ap", MakeNode("cons"), left), right);
    }
    int sign = 1;
    if (cur == "10") {
      sign = -1;
    }
    int bits = 0;
    while (ptr < (int) modulated.size() && modulated[ptr] == '1') {
      bits += 4;
      ptr += 1;
    }
    assert(ptr < (int) modulated.size());
    assert(modulated[ptr] == '0');
    ptr += 1;
    long long num = 0;
    for (int i = bits - 1; i >= 0; i--) {
      assert(ptr < (int) modulated.size());
      if (modulated[ptr] == '1') {
        num += 1LL << i;
      }
      ptr += 1;
    }
    return MakeNode(to_string(num * sign));
  };
  Node* ret = Dfs();
  assert(ptr == (int) modulated.size());
  return ret;
}

int main() {
  string line;
  vector<Node*> to_eval;
  while (getline(cin, line)) {
    stringstream ss;
    ss << line;
    vector<string> tokens;
    string token;
    while (ss >> token) {
      tokens.push_back(token);
    }
    if (tokens.empty()) {
      continue;
    }
    if (tokens.size() >= 2 && tokens[1] == "=") {
      int ptr = 2;
      function<Node*()> Dfs = [&]() {
        string cur = tokens[ptr++];
        if (cur == "ap") {
          Node* left = Dfs();
          Node* right = Dfs();
          return MakeNode(cur, left, right);
        }
        return MakeNode(cur);
      };
      Node* me = Dfs();
      assert(ptr == (int) tokens.size());
//      string str = me->repr();
//      cout << tokens[0] << " " << tokens[1] << " " << "lolnope" << '\n';
      auto iter = functions.find(tokens[0]);
      if (iter == functions.end()) {
        functions[tokens[0]] = me;
      } else {
        iter->second->text = me->text;
        iter->second->left = me->left;
        iter->second->right = me->right;
      }
    } else {
      int ptr = 0;
      function<Node*()> Dfs = [&]() {
        string cur = tokens[ptr++];
        if (cur == "ap") {
          Node* left = Dfs();
          Node* right = Dfs();
          return MakeNode(cur, left, right);
        }
        return MakeNode(cur);
      };
      Node* me = Dfs();
      to_eval.push_back(me);
//      string str = me->repr();
      cout << "lolnope" << '\n';
    }
  }
  cout << "-----" << '\n';
  for (Node* me : to_eval) {
    me->eval();
    cout << "done lol" << '\n';
//    continue;
    cout << me->unlist() << '\n';
    cout << me->unlist_ap() << '\n';
/*    cout << "full: " << me->repr() << '\n';
    int idx = 0;
    while (true) {
      Node* check = MakeNode("ap", MakeNode("isnil"), me);
      check->eval();
      if (check->text == "t") {
        break;
      }
      Node* first = MakeNode("ap", MakeNode("car"), me);
      first->eval();
      cout << ++idx << ": " << first->repr() << '\n';
      me = MakeNode("ap", MakeNode("cdr"), me);
    }
    cout << "done" << '\n';*/
  }
  return 0;
}
